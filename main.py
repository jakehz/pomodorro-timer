import time

FOCUS = 0
REST = 1


def secs_to_time(seconds: int):
    hours = seconds // (60 * 60)
    seconds = seconds % (60 * 60)
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{hours:03}:{minutes:02}:{seconds:02}"


def timer(seconds: int):
    while seconds:
        yield seconds
        time.sleep(1)
        seconds -= 1


def clear_line():
    print(f"\r{' '*100}", end="", flush=True)


def clear_prev_n_line(n):
    for _ in range(n):
        print(f"\033[F\r{' '*100}", end="", flush=True)


def get_durations_str(total_time: dict) -> str:
    return f"""
You have focused for: {secs_to_time(total_time[FOCUS])}
You have rested for: {secs_to_time(total_time[REST])}"""


def main():
    focus = ("Focus!", 25 * 60, FOCUS)
    short_rest = ("Take a short break", 5 * 60, REST)
    long_rest = ("Take a long break", 15 * 60, REST)

    order = [focus, short_rest, focus, short_rest, focus, long_rest]
    curr = 0
    total_focus = {FOCUS: 0, REST: 0}
    while True:
        if curr >= len(order):
            curr = 0
        msg, duration, period_type = order[curr]
        for curr_time in timer(duration):
            clear_line()
            print("\r" + secs_to_time(curr_time) + f" - {msg} ", end="", flush=True)

        total_focus[period_type] += duration
        clear_line()
        print(get_durations_str(total_focus))
        print(
            "\r Continue? Y/n: ",
            end="",
            flush=True,
        )
        response = input()
        # clear prev_line because user input has newline in it
        clear_prev_n_line(4)
        if response.lower() == "n":
            break
        curr += 1


if __name__ == "__main__":
    main()
