import datetime
def decryption(keys,data):
    dec_dict={}
    for j in range(len(keys)//2):
        dec_dict[keys[j]]=keys[len(keys)//2+j]

    dec_date=''
    for k in range(len(data)):
        dec_date+=dec_dict[data[k]]
    return dec_date

s_keys='Vj3JrGDuYnRLP04032,-54%+.61798'

s_data_tb='ZmJHXZmCqXZmZMXqMCMXJJCOXjZjmXjqMMXJHCqXZEJMXZjCZXJmqmXJMHOXjqMMXJOqjXJOmJXZJCqXZmEEXJmOMXJmCHXJCEJXJqjHXJOZMXZMMEXZjEZXjCjEXjCZZXJHZqXjCMEXjZmmXZjqEXZqMJXJOCOXJjqMXJHEZXJOOMXJOmmXZJZMXZMqJXJZmHXJOMCXjCjHXZOCjXZmOCXZmZjXZmjZXZqCjXZJmqXZjHJXOOHJXOqjqXmEqMXZMjMXOZMZXOJqZXOOMJXOEmqXOmEZXmCHmXZOCHXjOmJXjOjZXjJZJXjHEZXjHqZXZMCZXZJEOXOCjHXEqCjXMqCEXOJOqXOmZmXZJmHXZJjJXjjjqXJEHMXJEqEXJOOZXJOECXZmjHXZmCjXJJqmXJqMCXJmEHXJJMCXJqqCXZmCCXZZJOXJJmEXJmHqXJCjHXqHEEXJCmZXZCMEXHMEXZZHCXJCHZXqEOMXqHEHXqOJZXZZmOXZZZCXqHjqXJmZZXqHZOXJCCHXqHOOXZmOOXZmJOXJZOOXJJmEXJCECXJZqjXqHOJXZmOmXZjMqXJmOjXqEOHXqHHCXJCqJXqOqHXZCMZXZCEjXZZHqXHHZXZZEmXqHZOXJCjqXZOqqXZZCjXJCqMXqEEOXqMCmXqjqHXqEjmXZmJZXZCjqXJZCZXqHHmXqEEHXqEqjXqjOEXZCZJXEMHXqmEHXJZZOXJMZMXJJjmXJqOqXZmCHXZZCHXqHjEXqHHHXqHMmXJCZjXqECEXZZOOXZCJmXqjZOXqjCjXqjJCXqMZMXqJMmXZCmmXHCZXZCjqXqJmqXqjHZXqEmJXqMqZXZZEJXHEOXqHmEXqHmOXqECHXqjECXqOMHXZmjqXEOjXqMCEXqOMjXqOOqXJCZHXqHEZXZmqMXZCjqXqMCZXqOOHXqEmqXqHCJXqECOXZZHMXHCHXqHmEXJZHMXqMMJXqHZmXqjEZXZZmqXHCjXqOmMXqOjCXqjMqXqOHmXqmJqXZCZjXMMEXJZqEXJMZjXjCZmXJqmCXJZOCXZZJHXHZCXJCCMXJCJjXqMqJXqOOjXqmmMXHHCXEMEXqjHMXqOHZXqOqMXqJqEXqZjMXZCCmXMEjXmEZCXqJOZXqMZMXqJCHXqMZMXZZCCXHOZXqOjMXqMmOXqHJOXqOJOXqqOEXHHmXEMMXqjEMXqOqqXqEMJXqEqmXqjCOXZCOEXHOMXqMqHXqHCHXqOjEXqJMZXqjHjXZCEqXHCjXqmmmXqmZHXqCMmXmHOjXmHmMXZZHCXMHqXEHjXMJJXmHJJXmOOHXmjqHXHJmXZZCHXmEJqXmOOCXmJjEXmZMZXOJZXJMjXjCHXJMHXJMqXJHOXjHjXmqmjXZZOCXOHqXmqOCXmmHqXmqCEXmqCHXmmZqXOJmXjJZXmmCjXmmCMXmqmMXZEqjXZHmHXOMmXjJHXmCOOXmZEqXZHmCXmZqmXZHOqXOMOXjZqXZHHmXZHEOXmCCMXmCCjXmCHCXOJZXjMMXmCMZXmZmZXmCOCXmZHOXmZJMXMZqXjJZXmZHqXmZCOXmCEqXmCCjXmZZEXMCjXOjOXmmZMXmZJMXmZZHXmqjEXmZjCXMjJXjHZXmZCHXmZCjXmCJOXZHHmXZHqEXOJOXjjqXmZCHXmZCOXmmCHXmOHZXqjEOXZmOOXZmqqXqOZHXmOJOXmJZJXmjOHXmqEMXOjCXjJmXmZEHXmqmjXmmqqXmZEZXmCZqXjOqXjZjXmCOCXmCqjXZHmMXmCCjXZHMC'


s_return_tb=decryption(s_keys,s_data_tb)

with open("tb.csv","at") as f:
    f.write(s_return_tb+",")

