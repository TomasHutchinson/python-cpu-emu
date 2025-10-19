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
        STA F1              
        LDA F0              
        STA F0              
        BRA LOOP            

PROGRAM_END LDA F1          
            OUT             
            END             

N       DAT 000             
F0      DAT 000             
F1      DAT 000             
ZERO    DAT 000             
ONE     DAT 001             
TWO     DAT 002             
