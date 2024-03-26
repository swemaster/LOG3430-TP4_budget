import os

badhash = "c1a4be04b972b6c17db242fc37752ad517c29402"
goodhash = "e4cfc6f77ebbe2e23550ddab682316ab4ce1c03c"
MAX_ITERATIONS = 10
STOP_ON_FIRST_BAD_COMMIT = "first bad commit"

os.system("git bisect start " + badhash + " " + goodhash)

for i in range(MAX_ITERATIONS):
    current_hash = os.popen("git rev-parse HEAD").read().strip()
    result = os.system("python3 manage.py test")

    if result == 0:
        os.system("git bisect good " + current_hash)
    else:
        os.system("git bisect bad " + current_hash)

    if STOP_ON_FIRST_BAD_COMMIT in os.popen("git bisect log").read().lower():
        os.system("git bisect reset")
        print("\n\n\033[92mFirst bad commit: " + current_hash + "\033[0m")
        exit(1)

    if i == MAX_ITERATIONS - 1:
        print("\033[91mNo bad commit found after max number of iterations.\033[0m")
        break

os.system("git bisect reset")
exit(1)
