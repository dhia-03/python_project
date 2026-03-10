#!/usr/bin/env python3
"""Quick test to verify TCP flag checking logic"""

# Test the string checking logic
test_flags = ['S', 'SA', 'A', 'PA', 'F', '', 'RA']

for flags in test_flags:
    tcp_flags_str = str(flags)
    has_syn = 'S' in tcp_flags_str
    has_ack = 'A' in tcp_flags_str
    is_pure_syn = has_syn and not has_ack
    
    print(f"Flags: '{tcp_flags_str:3}' | has_syn={has_syn} | has_ack={has_ack} | pure_syn={'YES' if is_pure_syn else 'NO'}")
