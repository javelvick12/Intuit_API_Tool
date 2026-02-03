########### Admin/Import/Etc ###########
# utilities to be used generally

########### Deliverable ###########
#super helpful basic/standrad error code function
def print_error(e, f="UNKNOWN"):
    """
    Helpful basic/standrad error code function. Called withing code via a try and except block.
    """
    print("Error in %s!" % (f))
    print(e)
    print(type(e))

#call error with try/except within other functions
#def function():
#     """
#    Words.
#     """
#     try:
#   	<logic>
#     except Exception as e:
#         print_error(e, f="<function name>")
#         return None

########### Main ###########
def main():
    pass

if __name__ == '__main__':
    main()
