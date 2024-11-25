# This will be the file where I write the print scripts for the application title
# they will be imported into the main script. I do not want that script getting too cluttered

def print_title():
    return """
=====================================================================

   # # #    #    # #  # # #    ##       ##     ###     #    ##   #  
  #       #   #  # #  #       #  #      ##    #   #  #   #  ###  #
  # # #   # # #  # #  # #      #        ##    #   #  # # #  ###### 
       #  #   #  # #  #       #  ##     ##    #   #  #   #  ## ###
  # # #   #   #   #   # # #    # #      #####  ###   #   #  ##  ##

=====================================================================
"""

def print_about():
    return """
======================================================================
WRITTEN BY ANDREW RAWSON, 2024.
----------------------------------------------------------------------
This is a calculator program that can do many financial calculations.
It can find interest and monthly loan payments and dividends for 
certificates & money market accounts.

It has a table reference for dividends where the return is based on
account balances. You could also use the certificate path to calculate 
returns on a standard savings account since you enter the value for 
the interest rate.

Just follow the prompts and the program will do the work!

Have fun and thanks for using my program!

======================================================================
Start by choosing either a loan, or a savings product.
======================================================================
"""

def print_exit():
    return """ 
======================================================================
Closing program. See you next time!
======================================================================
    """
