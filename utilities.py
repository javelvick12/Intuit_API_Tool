########### Admin/Import/Etc ###########
import time

########### Deliverable ###########

def print_error(e, f="UNKNOWN"):
    print("Error in %s!" % (f))
    print(e)
    print(type(e))

def format_time(seconds):
    """
    Formats time in seconds, goes deep for computationally fast solutions.
    """
    try:
        if seconds is None:
            return "Not Measured"
        if seconds < 0.001:
            return f"{seconds * 1000000:.2f} microseconds"
        elif seconds < 1:
            return f"{seconds * 1000:.2f} milliseconds"
        else:
            return f"{seconds:.4f} seconds" 
    except Exception as e:
        print_error(e, f="format_time():")

########### Main ###########
def main():
    pass

if __name__ == '__main__':
    main()