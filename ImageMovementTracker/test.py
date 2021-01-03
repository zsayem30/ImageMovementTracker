from implementation import is_triangular_path
from sys import argv

data = [ ( 'assets/tree-cover-square-path-0.gif'  , 'square'   ), 
         ( 'assets/tree-cover-square-path-1.gif'  , 'square'   ), 
         ( 'assets/tree-cover-triangle-path-0.gif', 'triangle' ),
         ( 'assets/tree-cover-triangle-path-1.gif', 'triangle' ) ]

def run_test( filename, result ):
    expected_boolean = True if result == 'triangle' else False

    print( f'running test on file located at {filename}, expecting a {result} path!' )
    
    if is_triangular_path( filename ) == expected_boolean:
        print( 'test passed!' )
        return True
    else:
        print( 'test failed!' )
        return False

if __name__ == '__main__':
    argc = len( argv )

    if argc > 2:
        print( 'input error: provided either no arguments to run all tests or an integer index to run a specific test' )
        exit( 1 )

    # if an index is provided then test only that index
    if argc > 1:
        index = int( argv[1] )

        if index >= len( data ) or index < 0:
            print( f'index must be between 0 and {len(data) - 1} (inclusive).' )
            exit( 1 )

        filename, result = data[index]

        if run_test( filename, result ):
            exit( 0 )
        else:
            exit( 1 )
    else:
        passed_all = True

        for filename, result in data:
            if run_test( filename, result ) == False:
                passed_all = False

        if passed_all:
            exit( 0 )
        else:
            exit( 1 )




         
