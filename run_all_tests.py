#!/usr/bin/env python3
"""
Comprehensive test runner for error recovery in Little Duck compiler
"""
import ply.lex as lex
import ply.yacc as yacc
import sys

# Import the parser
exec(open('main_improved.py').read())

def run_test(filename, expected_desc):
    """Run a single test file and report results"""
    global lexer_errors, parser_errors
    lexer_errors = []
    parser_errors = []

    print("\n" + "="*80)
    print(f"📝 TEST: {filename}")
    print(f"Expected: {expected_desc}")
    print("="*80)

    try:
        with open(filename, 'r') as f:
            codigo = f.read()

        print("\n📄 CODE:")
        print("-"*80)
        for i, line in enumerate(codigo.split('\n'), 1):
            # Highlight lines with obvious errors
            marker = ""
            if any(c in line for c in [';;', '++', '**', ',,']) or \
               line.strip().endswith(('+', '-', '*', '/', ',', '(')):
                marker = " ← ERROR"
            print(f"{i:3d} | {line}{marker}")
        print("-"*80)

        # Create new lexer and parse
        test_lexer = lex.lex()
        test_lexer.lineno = 1
        resultado = parser.parse(codigo, lexer=test_lexer)

        total = len(lexer_errors) + len(parser_errors)

        print(f"\n📊 RESULTS:")
        if total == 0:
            print("   ✅ NO ERRORS - Program is valid!")
        else:
            print(f"   Total errors found: {total}")
            print(f"   - Lexical errors: {len(lexer_errors)}")
            print(f"   - Syntax errors: {len(parser_errors)}")

            print("\n   📋 Detailed errors:")
            for i, err in enumerate(lexer_errors + parser_errors, 1):
                print(f"      {i}. {err}")

        return total

    except FileNotFoundError:
        print(f"   ❌ FILE NOT FOUND: {filename}")
        return -1
    except Exception as e:
        print(f"   ❌ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        return -1

def main():
    """Run all tests"""
    print("="*80)
    print("LITTLE DUCK COMPILER - ERROR RECOVERY TEST SUITE")
    print("="*80)

    tests = [
        ("test_valid_program.txt", "Valid program, NO errors expected"),
        ("factorial.txt", "2 errors: stray 'claude' token"),
        ("test_expression_errors.txt", "2+ errors: malformed expressions"),
        ("test_function_errors.txt", "2+ errors: function definition problems"),
        ("test_if_while_errors.txt", "2+ errors: missing ) and incomplete while"),
        ("test_mixed_errors.txt", "4+ errors: mix of different error types"),
        ("test_call_errors.txt", "2+ errors: function call problems"),
        ("test_multiple_errors.txt", "2+ errors: multiple statement errors"),
    ]

    results = []
    for filename, desc in tests:
        error_count = run_test(filename, desc)
        results.append((filename, error_count))

    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    print(f"{'Test File':<40} {'Errors Found':>15}")
    print("-"*80)
    for filename, count in results:
        status = "✅ VALID" if count == 0 else f"❌ {count} errors"
        if count < 0:
            status = "⚠️  FAILED"
        print(f"{filename:<40} {status:>15}")

    print("="*80)
    print("TESTING COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
