#!/usr/bin/env python3
"""
AI Code Quality Gate - Detects AI-generated code patterns in pull requests
Analyzes code diffs for common indicators of low-quality AI-generated code
"""

import re
import sys
import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


class AICodeDetector:
    """Detects patterns commonly found in AI-generated code"""
    
    def __init__(self, threshold: int = 50):
        self.threshold = threshold
        self.issues = []
        
    def analyze_diff(self, diff_content: str) -> Dict:
        """Analyze a git diff for AI slop indicators"""
        score = 0
        added_lines = self._extract_added_lines(diff_content)
        
        # Run all detection heuristics
        score += self._check_generic_names(added_lines)
        score += self._check_excessive_comments(added_lines)
        score += self._check_pattern_repetition(added_lines)
        score += self._check_obvious_todos(added_lines)
        score += self._check_overly_verbose(added_lines)
        score += self._check_placeholder_logic(added_lines)
        
        return {
            "score": score,
            "threshold": self.threshold,
            "passed": score < self.threshold,
            "issues": self.issues,
            "lines_analyzed": len(added_lines)
        }
    
    def _extract_added_lines(self, diff: str) -> List[str]:
        """Extract only added lines from diff"""
        lines = []
        for line in diff.split('\n'):
            if line.startswith('+') and not line.startswith('+++'):
                lines.append(line[1:].strip())
        return lines
    
    def _check_generic_names(self, lines: List[str]) -> int:
        """Detect generic variable names like data, result, temp, item"""
        generic_patterns = r'\b(data|result|temp|item|value|obj|thing|stuff|info|val)\d*\b'
        score = 0
        for line in lines:
            matches = re.findall(generic_patterns, line, re.IGNORECASE)
            if matches:
                score += len(matches) * 5
                self.issues.append(f"Generic variable names found: {', '.join(set(matches))}")
        return min(score, 30)
    
    def _check_excessive_comments(self, lines: List[str]) -> int:
        """Check for excessive or obvious comments"""
        comment_lines = [l for l in lines if l.strip().startswith(('#', '//', '/*', '*'))]
        code_lines = [l for l in lines if l.strip() and not l.strip().startswith(('#', '//', '/*', '*'))]
        
        if not code_lines:
            return 0
            
        ratio = len(comment_lines) / len(code_lines)
        if ratio > 0.5:
            score = 20
            self.issues.append(f"Excessive comments: {len(comment_lines)} comments for {len(code_lines)} code lines")
            return score
        return 0
    
    def _check_pattern_repetition(self, lines: List[str]) -> int:
        """Detect repetitive code patterns"""
        # Check for repeated similar lines
        normalized = [re.sub(r'\d+', 'N', re.sub(r'["\'].*?["\']', 'STR', l)) for l in lines]
        unique_ratio = len(set(normalized)) / max(len(normalized), 1)
        
        if unique_ratio < 0.6 and len(lines) > 10:
            score = 25
            self.issues.append(f"High pattern repetition detected: {(1-unique_ratio)*100:.1f}% similar lines")
            return score
        return 0
    
    def _check_obvious_todos(self, lines: List[str]) -> int:
        """Check for TODO/FIXME/HACK comments"""
        todo_pattern = r'(TODO|FIXME|HACK|XXX|PLACEHOLDER)'
        score = 0
        for line in lines:
            if re.search(todo_pattern, line, re.IGNORECASE):
                score += 10
                self.issues.append(f"Placeholder comment found: {line[:60]}")
        return min(score, 20)
    
    def _check_overly_verbose(self, lines: List[str]) -> int:
        """Detect overly verbose or explanatory code"""
        verbose_patterns = [
            r'# (First|Then|Next|Finally|Now),',
            r'# Step \d+:',
            r'# This (function|method|class) (will|does|is)',
        ]
        score = 0
        for line in lines:
            for pattern in verbose_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    score += 8
                    self.issues.append(f"Overly verbose comment: {line[:60]}")
        return min(score, 25)
    
    def _check_placeholder_logic(self, lines: List[str]) -> int:
        """Check for placeholder or incomplete logic"""
        placeholders = [r'pass\s*$', r'return None\s*$', r'\.\.\.\s*$', r'raise NotImplementedError']
        score = 0
        for line in lines:
            for pattern in placeholders:
                if re.search(pattern, line):
                    score += 15
                    self.issues.append(f"Placeholder logic: {line[:60]}")
        return min(score, 30)


def main():
    parser = argparse.ArgumentParser(
        description='AI Code Quality Gate - Detect AI-generated code patterns'
    )
    parser.add_argument('diff_file', help='Path to git diff file')
    parser.add_argument('--threshold', type=int, default=50,
                       help='Quality threshold (0-100, lower is stricter)')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')
    
    args = parser.parse_args()
    
    # Read diff file
    try:
        diff_content = Path(args.diff_file).read_text()
    except FileNotFoundError:
        print(f"Error: File '{args.diff_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Analyze
    detector = AICodeDetector(threshold=args.threshold)
    results = detector.analyze_diff(diff_content)
    
    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\n🔍 AI Code Quality Analysis")
        print(f"{'='*50}")
        print(f"Lines analyzed: {results['lines_analyzed']}")
        print(f"Quality score: {results['score']}/{results['threshold']}")
        print(f"Status: {'✅ PASSED' if results['passed'] else '❌ FAILED'}\n")
        
        if results['issues']:
            print("Issues found:")
            for issue in results['issues'][:10]:
                print(f"  • {issue}")
    
    sys.exit(0 if results['passed'] else 1)


if __name__ == '__main__':
    main()