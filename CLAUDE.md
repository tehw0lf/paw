# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**paw** (patterns and wordlists in python) is a password pattern analysis and wordlist generation tool. It analyzes password patterns from input files and generates custom wordlists based on character sets, with support for generating hashcat commands for optimized brute force attacks.

## Architecture

### Core Components

- **`paw/core.py`**: Main `Paw` class that orchestrates pattern analysis and wordlist generation
  - Delegates wordlist generation to `wlgen` library (external dependency)
  - Supports 3 algorithms (0: itertools.product, 1: in-memory, 2: on-the-fly)
  - Maintains state: `patterns` (detected patterns by length), `cset` (character sets), `catstrs` (hashcat commands)

- **`paw/patterns.py`**: Pattern detection and hashcat command generation
  - `cset_lookup()`: Maps characters to standard character sets (d/u/l/h/i/s)
  - `generate_pattern()`: Builds patterns from input strings by analyzing character types
  - `generate_hcat_command()`: Converts patterns to hashcat mask attack commands
  - `parse_charsets()`: Parses bracket notation `[ABC][123]` into character sets

- **`paw/wordlist.py`**: File I/O for wordlist generation
  - `save_to_file()`: Buffers and writes wordlists to files or stdout
  - Calculates total wordlist size using combinatorial math

- **`paw/static.py`**: Standard character set definitions
  - `d`: digits (0-9)
  - `u`: uppercase letters (including German umlauts)
  - `l`: lowercase letters (including German umlauts)
  - `h`: uppercase hex (ABCDEF)
  - `i`: lowercase hex (abcdef)
  - `s`: special characters

- **`paw/command_line.py`**: CLI argument parsing and orchestration
  - Entry point for `paw` command
  - Validates argument combinations (mutual exclusivity of `-p`, `-g`, `-c`)

### Workflow Patterns

1. **Pattern from passwords** (`-p`):
   - Read passwords → detect patterns → optionally generate hashcat commands
   - Patterns are merged by string length

2. **Wordlist from generated charsets** (`-g`):
   - Parse bracket notation → replace `%x` with standard charsets → generate wordlist

3. **Wordlist from file charsets** (`-c`):
   - Read charsets from file (line = position) → detect patterns → generate wordlist → optionally generate hashcat commands

## Development Commands

### Setup
```bash
uv sync                  # Install dependencies from uv.lock
uv sync --all-extras --dev --group lint  # Install with all extras and dev dependencies
```

### Testing
```bash
uv run python -m unittest discover       # Run all tests
uv run python -m unittest paw.tests.test_gen_wordlist  # Run specific test module
```

### Linting
```bash
uv run ruff check        # Lint with Ruff
uv run ruff format       # Format code
```

### Building
```bash
uv build                 # Build wheel and sdist in dist/
```

### Running CLI
```bash
uv run paw -h            # Show help
uv run paw -p -i input.txt                    # Pattern from passwords
uv run paw -g '[%d%l][%u]' -o wordlist.txt    # Generate wordlist from charsets (auto algorithm)
uv run paw -g '[%d%l][%u]' -a 0 -o out.txt    # Generate with specific algorithm (0=iter, 1=list, 2=words)
uv run paw -c -i charsets.txt -o out.txt      # Generate from file charsets
uv run paw -p -i input.txt -H                 # Generate hashcat commands
```

## Pre-commit Validation

**IMPORTANT**: Run these commands before committing:

```bash
uv run ruff check && uv run python -m unittest discover && uv build
```

All commands must exit with code 0.

## CI/CD

Uses reusable workflow from `tehw0lf/workflows` with:
- Tool: `uv`
- Lint: `uv run ruff check`
- Test: `uv run python -m unittest discover`
- Build: `uv build`
- Publishes GitHub releases and artifacts from `dist/` directory

## Testing Structure

- **Base class**: `paw/tests/base.py` provides `paw_test(unittest.TestCase)` with shared setup
- Tests use `unittest` framework (not pytest)
- Test files in `paw/tests/test_files/` contain fixtures for pattern and wordlist tests

## Key Design Considerations

### Character Set System
- Standard charsets use `%` prefix (`%d`, `%l`, `%u`, etc.)
- Patterns combine multiple charset types (e.g., `%du` = digits + uppercase)
- Bracket notation allows position-specific charsets: `[%d%l][%u]` = "aA", "aB", ..., "zZ"

### Hashcat Integration
- Hashcat supports only 2 custom charsets (`-1`, `-2`)
- Paw maps `%h` (upper hex) → `-1` and `%i` (lower hex) → `-2`
- Generated commands use `-a 3` (brute force mask attack)

### Algorithm Selection
- **'auto' (default)**: Smart selection based on problem size (leverages `wlgen.generate_wordlist`)
  - <1K combinations: Uses in-memory list generation (fastest)
  - 1K-100K combinations: Uses in-memory list generation (fast + convenient)
  - >100K combinations: Uses `itertools.product` (optimal throughput)
- **Algorithm 0**: Forces `gen_wordlist_iter` (memory-efficient, ~780-810K comb/s)
- **Algorithm 1**: Forces `gen_wordlist` (fast for small lists, ~900K-1.6M comb/s, high memory)
- **Algorithm 2**: Forces `gen_words` (slowest, ~210-230K comb/s, minimal memory footprint)

**Recommendation**: Use default 'auto' for most cases. Only specify `-a` flag if you have specific memory or performance constraints.

## Dependencies

- **wlgen**: External wordlist generation library (>=2.0.0)
  - Provides `gen_wordlist_iter`, `gen_wordlist`, `gen_words` functions
  - Must be installed for paw to function
