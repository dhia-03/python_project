#!/usr/bin/env python3
"""
Quick test script to verify detection engine works with sample data
"""
from TrafficAnalyzer import TrafficAnalyzer
from DetectionEngine import DetectionEngine

print("=" * 60)
print("Testing Detection Engine Logic")
print("=" * 60)

analyzer = TrafficAnalyzer()
detector = DetectionEngine()

# Simulate scanning 15 ports (threshold is 10)
print("\nSimulating port scan: scanning 15 ports...")
for port in range(20, 35):
    # Create mock features as if from a real packet
    features = {
        'src_ip': '192.168.1.100',
        'dst_ip': '192.168.1.1',
        'src_port': 12345,
        'dst_port': port,
        'protocol': 'TCP',
        'tcp_flags': 'S'
    }
    
    threats = detector.detect_threats(features)
    
    if threats:
        print(f"\n✓ THREAT DETECTED after {port - 19} ports!")
        for threat in threats:
            print(f"  - Type: {threat['rule']}")
            print(f"  - Confidence: {threat['confidence']}")
        break
else:
    print("\n✗ No threats detected - something is wrong!")

print("\n" + "=" * 60)
