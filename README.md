# AI Code Quality Gate CLI

🛡️ **Automatically detect and filter low-quality AI-generated code in pull requests**

Stop wasting reviewer time on "AI slop" - generic variable names, excessive comments, repetitive patterns, and placeholder logic that AI code generators often produce.

## The Problem

AI code generation tools are flooding repositories with low-quality contributions. Open-source projects like Godot are drowning in AI-generated PRs that waste maintainer time. This CLI tool helps you automatically detect common AI code patterns before they reach human review.

## Features

✅ Detects generic variable names (data, result, temp, item)
✅ Identifies excessive or obvious comments
✅ Finds repetitive code patterns
✅ Spots placeholder logic (TODO, pass, NotImplementedError)
✅ Catches overly verbose explanatory comments
✅ JSON output for CI/CD integration
✅ Configurable quality thresholds

## Installation

```bash
pip install ai-code-quality-gate
```

Or clone and run directly:

```bash
git clone https://github.com/LuluFoxy-AI/ai-generated-code-quality-gate-cli.git
cd ai-generated-code-quality-gate-cli
python ai_quality_gate.py <diff_file>
```

## Usage

### Basic Usage

```bash
# Analyze a git diff
git diff main > changes.diff
ai-quality-gate changes.diff
```

### GitHub Actions Integration

```yaml
name: AI Code Quality Check
on: [pull_request]

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Get PR diff
        run: git diff origin/main > pr.diff
      - name: Run AI Quality Gate
        run: |
          pip install ai-code-quality-gate
          ai-quality-gate pr.diff --threshold 50
```

### Configuration

```bash
# Adjust threshold (0-100, lower is stricter)
ai-quality-gate changes.diff --threshold 30

# JSON output for parsing
ai-quality-gate changes.diff --json
```

## Free vs Pro

**Free (Open Source)**
- ✅ All core detection features
- ✅ CLI tool
- ✅ GitHub Actions integration
- ✅ Unlimited open-source repos

**Pro ($49/month per repo)**
- ✅ Everything in Free
- ✅ Private repository support
- ✅ Custom detection rules
- ✅ Team dashboard
- ✅ Priority support

**Enterprise ($299/month)**
- ✅ Everything in Pro
- ✅ Unlimited private repos
- ✅ Self-hosted option
- ✅ Advanced analytics
- ✅ SLA support

## License

MIT License - Free for open-source projects

Commercial use in private repositories requires a Pro license.