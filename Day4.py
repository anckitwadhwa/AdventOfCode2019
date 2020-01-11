def check_for_2_adjacent_digits_are_same (Number):
    NumberAsString = str(Number)
    Are2AdjacentDigitsSame = False
    Index = 1

    while (Index < len (NumberAsString)):
        LeftDigit = int(NumberAsString[Index-1])
        RightDigit = int(NumberAsString[Index])

        #print (LeftDigit, RightDigit)

        if (LeftDigit == RightDigit):
            Are2AdjacentDigitsSame = True
            break

        Index += 1

    return Are2AdjacentDigitsSame


def check_for_exactly_2_adjacent_digits_are_same (Number):
    NumberAsString = str(Number)
    AreExactly2AdjacentDigitsSame = False
    Index = 1

    while (Index < len (NumberAsString)):
        LeftDigit = int(NumberAsString[Index-1])
        RightDigit = int(NumberAsString[Index])

        #print (LeftDigit, RightDigit)

        if (LeftDigit == RightDigit):
            AreExactly2AdjacentDigitsSame = True;
            if (Index - 2 >= 0):
                LeftOfLeftDigit = int(NumberAsString[Index-2])

                if (LeftOfLeftDigit == LeftDigit):
                    AreExactly2AdjacentDigitsSame = False

            if (Index + 1 < len (NumberAsString)):
                RightOfRightDigit = int(NumberAsString[Index + 1])

                if (RightOfRightDigit == RightDigit):
                    AreExactly2AdjacentDigitsSame = False

        if (AreExactly2AdjacentDigitsSame):
            break

        Index += 1

    return AreExactly2AdjacentDigitsSame

def check_for_montonically_increasing_digits (Number):
    NumberAsString = str(Number)
    IsMonotonicallyIncreasing = True
    Index = 1

    while (Index < len (NumberAsString)):
        LeftDigit = int(NumberAsString[Index-1])
        RightDigit = int(NumberAsString[Index])

        #print (LeftDigit, RightDigit)

        if (LeftDigit > RightDigit):
            IsMonotonicallyIncreasing = False
            break

        Index += 1

    return IsMonotonicallyIncreasing



#TestNumber = 12345
#TestNumber = 123444
TestNumber = 123323335
#print (check_for_montonically_increasing_digits(TestNumber))
#print (check_for_2_adjacent_digits_being_same(TestNumber))
print (check_for_exactly_2_adjacent_digits_are_same(TestNumber))


StartNumber = 156218
StopNumber = 652527


NumbersThatMeetBothCriteria = 0
for Number in range (StartNumber, StopNumber):
    #if (check_for_montonically_increasing_digits (Number) & check_for_2_adjacent_digits_are_same(Number)):
    if (check_for_montonically_increasing_digits (Number) & check_for_exactly_2_adjacent_digits_are_same(Number)):
        NumbersThatMeetBothCriteria += 1

print (NumbersThatMeetBothCriteria)

