START   INP 0
        STA N
        LDA ZERO
        STA F0
        LDA ONE
        STA F1

LOOP    LDA N
        SUB ONE
        STA N
        BRZ PROGRAM_END
        LDA F1
        ADD F0
        STA TEMP
        LDA F1
        STA F0
        LDA TEMP
        STA F1
        BRA LOOP

PROGRAM_END LDA F1
        DIV TWO
        DIV TWO
        OUT
        END

N       DAT 0
F0      DAT 0
F1      DAT 0
TEMP    DAT 0
ZERO    DAT 0
ONE     DAT 1
TWO     DAT 2