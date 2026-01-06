#!/usr/bin/env python3
"""Test script for Superheroes API"""
import requests
import json
import time

base_url = 'http://localhost:5555'

def wait_for_server():
    """Wait for server to be ready"""
    for i in range(10):
        try:
            requests.get(f'{base_url}/heroes', timeout=1)
            return True
        except:
            time.sleep(1)
    return False

def test_api():
    print('='*60)
    print('TESTING SUPERHEROES API')
    print('='*60 + '\n')
    
    # Test 1
    print('✓ Test 1: GET /heroes')
    r = requests.get(f'{base_url}/heroes')
    assert r.status_code == 200
    heroes = r.json()
    print(f'  Status: {r.status_code} ✓')
    print(f'  Result: {len(heroes)} heroes')
    print(f'  Sample: {heroes[0]}\n')
    
    # Test 2
    print('✓ Test 2: GET /heroes/1')
    r = requests.get(f'{base_url}/heroes/1')
    assert r.status_code == 200
    hero = r.json()
    print(f'  Status: {r.status_code} ✓')
    print(f'  Hero: {hero["name"]} - {hero["super_name"]}')
    print(f'  Powers: {len(hero.get("hero_powers", []))} power(s)\n')
    
    # Test 3
    print('✓ Test 3: GET /powers')
    r = requests.get(f'{base_url}/powers')
    assert r.status_code == 200
    powers = r.json()
    print(f'  Status: {r.status_code} ✓')
    print(f'  Result: {len(powers)} powers\n')
    
    # Test 4
    print('✓ Test 4: GET /powers/2')
    r = requests.get(f'{base_url}/powers/2')
    assert r.status_code == 200
    power = r.json()
    print(f'  Status: {r.status_code} ✓')
    print(f'  Power: {power["name"]}\n')
    
    # Test 5
    print('✓ Test 5: PATCH /powers/2')
    r = requests.patch(f'{base_url}/powers/2', 
                       json={'description': 'Updated: gives the wielder amazing flight abilities'},
                       headers={'Content-Type': 'application/json'})
    assert r.status_code == 200
    print(f'  Status: {r.status_code} ✓')
    print(f'  Updated successfully\n')
    
    # Test 6
    print('✓ Test 6: POST /hero_powers')
    r = requests.post(f'{base_url}/hero_powers',
                      json={'strength': 'Average', 'power_id': 3, 'hero_id': 4},
                      headers={'Content-Type': 'application/json'})
    assert r.status_code == 201
    hp = r.json()
    print(f'  Status: {r.status_code} ✓')
    print(f'  Created: {hp["hero"]["name"]} + {hp["power"]["name"]}\n')
    
    # Test 7 - Validation
    print('✓ Test 7: POST /hero_powers (invalid strength)')
    r = requests.post(f'{base_url}/hero_powers',
                      json={'strength': 'Super', 'power_id': 1, 'hero_id': 2},
                      headers={'Content-Type': 'application/json'})
    assert r.status_code == 400
    print(f'  Status: {r.status_code} ✓ (Expected 400)')
    print(f'  Validation working correctly\n')
    
    # Test 8 - Not found
    print('✓ Test 8: GET /heroes/999 (not found)')
    r = requests.get(f'{base_url}/heroes/999')
    assert r.status_code == 404
    print(f'  Status: {r.status_code} ✓ (Expected 404)\n')
    
    # Test 9 - Validation
    print('✓ Test 9: PATCH /powers/1 (short description)')
    r = requests.patch(f'{base_url}/powers/1',
                       json={'description': 'Too short'},
                       headers={'Content-Type': 'application/json'})
    assert r.status_code == 400
    print(f'  Status: {r.status_code} ✓ (Expected 400)\n')
    
    print('='*60)
    print('ALL 9 TESTS PASSED! ✓✓✓')
    print('='*60)

if __name__ == '__main__':
    print('Waiting for server to start...')
    if wait_for_server():
        print('Server is ready!\n')
        test_api()
    else:
        print('Server did not start. Please run: python app.py')
