"""
FUEL BATTLE
"""
from ai import ai_one, ai_two
from organizer import call as call_organizer
import ui

def main():
    call_organizer('A', 10**6, ai_one)
    call_organizer('B', 10**6, ai_two)

if __name__ == '__main__':
    main()




