from requests import get, post, delete
import sys


api_key = "676B5F7365637265745F6170695F6B6579"

print('get', '/api/users')
print(get('http://localhost:5000/api/users' + '|' + api_key).json())
print()
print('get', '/api/user/1')
print(get('http://localhost:5000/api/user/1' + '|' + api_key).json())
print()
print('get', '/api/user/9999999999')
print(get('http://localhost:5000/api/user/9999999999' + '|' + api_key).json())
print()
print('get', '/api/user/abc')
print(get('http://localhost:5000/api/user/abc' + '|' + api_key).json())
print()
print('get', '/api/users')
print(get('http://localhost:5000/api/users' + '|' + api_key).json())
print()
print('post', '/api/users')
print(post('http://localhost:5000/api/users' + '|' + api_key, json={
    'id': 9999999999,
    'name': 'test',
    'email': 'test@test.test',
    'permission': 'test',
    'password': 'test'
}).json())
print()
print('get', '/api/users')
print(get('http://localhost:5000/api/users' + '|' + api_key).json())
print()
print('delete', '/api/user/9999999999')
print(delete('http://localhost:5000/api/user/9999999999' + '|' + api_key).json())
print()
print('get', '/api/users')
print(get('http://localhost:5000/api/users' + '|' + api_key).json())

print('\n------------------------------------------------------------\n')

print('get', '/api/products')
print(get('http://localhost:5000/api/products' + '|' + api_key).json())
print()
print('get', '/api/product/1')
print(get('http://localhost:5000/api/product/1' + '|' + api_key).json())
print()
print('get', '/api/product/9999999999')
print(get('http://localhost:5000/api/product/9999999999' + '|' + api_key).json())
print()
print('get', '/api/product/abc')
print(get('http://localhost:5000/api/product/abc' + '|' + api_key).json())
print()
print('get', '/api/products')
print(get('http://localhost:5000/api/products' + '|' + api_key).json())
print()
print('post', '/api/products')
print(post('http://localhost:5000/api/products' + '|' + api_key, json={
    'id': 9999999999,
    'title': 'test',
    'short_about': 'test',
    'about': 'test',
    'price': 1,
    'purchased_content': 'test',
    'user_id': 1
}).json())
print()
print('get', '/api/products')
print(get('http://localhost:5000/api/products' + '|' + api_key).json())
print()
print('delete', '/api/product/9999999999')
print(delete('http://localhost:5000/api/product/9999999999' + '|' + api_key).json())
print()
print('get', '/api/products')
print(get('http://localhost:5000/api/products' + '|' + api_key).json())

print('\n------------------------------------------------------------\n')


print('get', '/api/categories')
print(get('http://localhost:5000/api/categories' + '|' + api_key).json())
print()
print('get', '/api/category/1')
print(get('http://localhost:5000/api/category/1' + '|' + api_key).json())
print()
print('get', '/api/category/9999999999')
print(get('http://localhost:5000/api/category/9999999999' + '|' + api_key).json())
print()
print('get', '/api/category/abc')
print(get('http://localhost:5000/api/category/abc' + '|' + api_key).json())
print()
print('get', '/api/categories')
print(get('http://localhost:5000/api/categories' + '|' + api_key).json())
print()
print('post', '/api/categories')
print(post('http://localhost:5000/api/categories' + '|' + api_key, json={
    'id': 9999999999,
    'name': 'test'
}).json())
print()
print('get', '/api/categories')
print(get('http://localhost:5000/api/categories' + '|' + api_key).json())
print()
print('delete', '/api/category/9999999999')
print(delete('http://localhost:5000/api/category/9999999999' + '|' + api_key).json())
print()
print('get', '/api/categories')
print(get('http://localhost:5000/api/categories' + '|' + api_key).json())

print('\n------------------------------------------------------------\n')

print('post', '/api/promocodes')
print(post('http://localhost:5000/api/promocodes' + '|' + api_key, json={
    'id': 9999999999,
    'content': 'test',
    'award': 1
}).json())
print()
print('delete', '/api/promocode/9999999999')
print(delete('http://localhost:5000/api/promocode/9999999999' + '|' + api_key).json())