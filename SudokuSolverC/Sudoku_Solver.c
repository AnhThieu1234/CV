
// Code : Here include your necessary library(s)
#include <stdio.h>
#include <stdbool.h>

// Code : Write your global variables here, like:
#define N 9
#define EMPTY 0
int count = 0;

/*Code : write your functions here, or the declaration of the function/
For example write the recursive function solveSudoku(), like:*/

//function to print array
void printArray(int arr[N][N]) {
    //for loop go through all rows
    for (int i=0;i<N;i++) {
        printf("\n");
        //for loop go through all cols
        for (int j=0;j<N;j++) {
            //print number at row & col
            printf("%d ",arr[i][j]);
            if (j == 2 || j == 5) {
                printf ("| ");
            }
        }
        if (i == 2 || i == 5) {
            printf("\n---------------------");
        }
    }
    printf("\n");
}

//function to check if a number is in that row
bool numInRow(int arr[N][N], int num, int numRow, int numCol){
    //for loop go through each col
    for (int i=0; i<N; i++) {
        //if any number exists in that row -> return true
        if ((arr[numRow][i] == num) && (i != numCol)) {
            return true;
        }
    }
    //if no number in that row -> return false
    return false;
}

//function to check if a number is in that col
bool numInCol(int arr[N][N], int num, int numRow, int numCol){
    //for loop go through each row
    for (int i=0; i<N; i++) {
        //if any number exists in that col -> return true
        if ((arr[i][numCol] == num) && (i != numRow)) {
            return true;
        }
    }
    //if no number in that col -> return false
    return false;
}

//function to check if a number is in respected 3x3 cell
bool numIn3x3(int arr[N][N], int num, int numRow, int numCol) {
    //initialize variables
    int rCheck = 0; // respected starting row for 3x3
    int cCheck = 0; // respected starting col for 3x3

    //switch cases to determine which 3x3 block (out of 9 3x3's) to check
    switch (numRow) {
        case 0 ... 2: // row is from 0 to 2
            rCheck = 0;
        break;
        case 3 ... 5: // row is from 3 to 5
            rCheck = 3;
        break;
        case 6 ... 8: // row is from 6 to 8
            rCheck = 6;
        break;
    }
    switch (numCol) {
        case 0 ... 2: // col is from 0 to 2
            cCheck = 0;
        break;
        case 3 ... 5: // col is from 3 to 5
            cCheck = 3;
        break;
        case 6 ... 8: // col is from 6 to 8
            cCheck = 6;
        break;
    }

    //for loop go from row to col + 3 (for 3x3 blocks)
    for (int i = rCheck; i<rCheck+3; i++) {
        //for loop go from col to col + 3 (for 3x3 blocks)
        for (int j = cCheck; j<cCheck+3; j++) {
            //if number exists in 3x3 block -> return true
            if ((num == arr[i][j]) && (i != numRow) && (j != numCol)) {
                return true;
            }
        }
    }
    //if number isn't in 3x3 block -> return false
    return false;
}

//function to check if all the slots in the sudoku puzzle is filled
bool emptySlots(int arr[N][N]) {
    //for loop go through rows of sudoku puzzle
    for (int i=0; i<N; i++) {
        //for loop go through cols of sudoku puzzle
        for (int j=0; j<N; j++) {
            //if that slot is EMPTY (0) -> return true
            if (arr[i][j] == EMPTY) {
                return true;
            }
        }
    }
    //if no slots are EMPTY (0) -> return false
    return false;
}

//function to solve sudoku puzzle using all helper functions
bool solveSudoku(int arr[N][N]) {
    //initialize variables to keep track of position
    int row;
    int col;

    //increase count of iteration
    count += 1;

    //use emptySlots() function to check if there progress
    if (emptySlots(arr) == false) {
        return true; // if all slots are filled -> solution found! -> return true
    }

    //for loop go through rows of sudoku
    for (row=0; row<N; row++) {
        //for loop go through cols of sudoku
        for (col=0; col<N; col++) {
            //checking if the current slot is an empty/mutable slot
            if (arr[row][col] == EMPTY) {
                //for loop go through numbers (1 to 9) -- call it a "trial #"
                for (int i=1; i<=N; i++) {
                    //using numInCol(), numInRow(), & numIn3x3() functions to check if the "trial #" is valid to be in that position (if no other numbers in row/col/3x3 = "trial #")
                    //if "trial #" is valid
                    if ((numInCol(arr,i,row,col) == false) && (numInRow(arr,i,row,col) == false) && (numIn3x3(arr,i,row,col) == false)) {
                        arr[row][col] = i; // change array at current position to "trial #"
                        
                        /*recursively call solveSudoku() function to check if 
                          the changed "trial #" will lead to a solution */
                        if (solveSudoku(arr) == true) { /*if solveSudoku(a) == true -> leads 
                                                          to a solution -> return true & stop*/
                            //final checking the whole puzzle in case input was incorrect
                            for (int c=0; c<N;c++) {
                                for (int b=0; b<N; b++) {
                                    if ((numInCol(arr,arr[c][b],c,b) == true) || (numInRow(arr,arr[c][b],c,b) == true) || (numIn3x3(arr,arr[c][b],c,b) == true)) {
                                        return false;
                                    }
                                }
                            }

                            return true; //puzzle is solved
                        } //if solve Sudoku(a) == false -> won't lead to a solution -> keep going

                        //no solution found with "trial #" so reset the slot to EMPTY (0) & backtrack (undo)
                        arr[row][col] = EMPTY;
                    }    
                }
                return false; //if no trial #'s (1 to 9) lead to a solution -> return false & stop recursion
            }
        }
    }
    return false; //if all possibilites have been tried but no solution -> return false & stop recrusion
}

//main code block
int main()
{

    // This is hard coding to receive the "arr"
    int grid[N][N] = {
        {0, 2, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 6, 0, 0, 0, 0, 3},
        {0, 7, 4, 0, 8, 0, 0, 0, 0},
        //---------------------------
        {0, 0, 0, 0, 0, 3, 0, 0, 2},
        {0, 8, 0, 0, 4, 0, 0, 1, 0},
        {6, 0, 0, 5, 0, 0, 0, 0, 0},
        //---------------------------
        {0, 0, 0, 0, 1, 0, 7, 8, 0},
        {5, 0, 0, 0, 0, 9, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 4, 0}};
        
    // For more samples to check your program, google for solved samples, or
    // check https://sandiway.arizona.edu/sudoku/examples.html

    printf("The input Sudoku puzzle:\n");
    // "print" is a function we define to print the "arr"
    printArray(grid);
    if (solveSudoku(grid) == true) 
    {
        // If the puzzle is solved then:
        printf("\nSolution found after %d iterations:", count);
        printArray(grid);
    }
    else
    {
        printf("\nNo solution exists.\n");
    }
    return 0;
}
