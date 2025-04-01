import sys

from Utils.read import read_contents

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')



for line in read_contents(read_contents(sys.stdin)):
    sys.stdout.write(line)