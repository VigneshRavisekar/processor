module control(input logic clk,rstn, input logic [4:0] ip, output logic [2:0] opcode, output logic isTrf,isRegWr,isOp,isFetchImm,isImm,isALU,isCmp,isStr,isLd,isMemSel,isMemWrite,sign_flag);

            

            typedef enum logic [3:0] {RESET = 0, FETCH = 1, DECODE = 2, FETCH_IMM = 3, EXECUTE_ALU = 4,UPDATE_FLAG=5, REGWRITE = 6,EXECUTE_MEM = 7} states_t;
            states_t state,next_state;

            logic [1:0] fielder;
            logic immediate;

            always_ff@(posedge clk or negedge rstn)
                if(!rstn)
                    state <= RESET;
                else
                    state <= next_state;

            always_comb begin 

                unique case(state)

                    RESET: 
                            next_state = FETCH;
                    
                    FETCH:
                        begin
                           
                           next_state = DECODE;
                           immediate = 0;
                        end 
                    DECODE:
                        begin 
                            
                            /* OPCODE IS 000 WHERE IT CONTAINS BOTH ADDITION AND TRANSFER OPERATION*/
                            if(ip[4:2]== 0) 
                            begin

                                if(ip[0] == 1) // Transfer bit selected

                                    begin

                                        if(ip[1] == 0) // Normal Transfer
                                                next_state = REGWRITE;
                                        else
                                            begin
                                                next_state = FETCH_IMM;
                                                // immediate = 1;
                                            end
                                    end


                                else // Addition bit selected

                                    begin 

                                        if(ip[1] == 0) // Normal Addition
                                                next_state = EXECUTE_ALU;
                                        
                                        else 
                                            begin
                                                next_state = FETCH_IMM;
                                                // immediate = 1;
                                            end 
                                    end 

                            end

                            /* OPCODE is 001/010/011/100/101 WHERE IT CONTAINS SUBTRACTION/AND/OR/NOT/CMP (Normal and Immediate Instructions)*/

                            else if(ip[4:2]==1 || ip[4:2] == 2 || ip[4:2] == 3 || ip[4:2] == 4 || ip[4:2] == 5)
                            begin

                                if(ip[1]==0) // Normal Sub/AND/OR/CMP
                                            next_state = EXECUTE_ALU;

                                else // Immediate Sub/AND/OR/CMP
                                begin

                                        next_state = FETCH_IMM;
                                        immediate = 1;
                                end
                            end
                            
                            /* OPCODE is 110 WHERE IT CONTAINS MEMORY STORE AND LOAD OPERATIONS*/
                            else if(ip[4:2] == 6) 
                            begin

                                            next_state = EXECUTE_MEM;
                                     
                            end


                            else 

                                    next_state = DECODE;
                            
                        end

                    EXECUTE_ALU: begin 

                                if(immediate == 0)
                                begin
                                    if(ip[4:2] == 5)
                                        next_state = UPDATE_FLAG;
                                    else
                                        next_state = REGWRITE;
                                end

                                else
                                begin 
                                    if(opcode == 5)
                                        next_state = UPDATE_FLAG;
                                    else
                                        next_state = REGWRITE;
                                end
                    end 
                    EXECUTE_MEM: begin

                                    if(ip[1] == 1) // Store Operation
                                        next_state = FETCH;
                                    else
                                        next_state = REGWRITE;
                    end 
                    
                    UPDATE_FLAG:

                                next_state = FETCH;
                    FETCH_IMM:
                    begin 
                            /* OPCODE 000 in Fetch_Imm to indicate Trf/Add Instruction
                            OPCODE 001 in Fetch_Imm to indicate Sub Instruction
                            OPCODE 010 in Fetch_Imm to indicate AND Instruction 
                            OPCODE 011 in Fetch_Imm to indicate OR Instruction
                            trf bit tell next_state for above all instructions 
                            
                            OPCODE 101 in Fetch_imm indicate Compare Instruction*/
                            if(ip[4:2]==0 || ip[4:2] == 1 || ip[4:2] == 2 || ip[4:2] == 3 || ip[4:2] == 4) 
                            begin
                                if(ip[0] == 0)
                                    next_state = EXECUTE_ALU;
                                else
                                    next_state = REGWRITE;
                            end

                            else if(ip[4:2] == 5)
                            begin
                                    next_state = EXECUTE_ALU;
                            end
                          

                    end   
                    
                    REGWRITE:
                               
                               next_state = FETCH;
                endcase
                    
            end
            
            always_comb begin
                
                unique case (state)

                    RESET: begin
                        {isTrf, isRegWr, isOp, isImm} = 4'b0000;
                        isFetchImm = 1'b0;
                    end

                    FETCH: begin
                        {isTrf, isRegWr, isOp, isImm} = 4'b0000;
                        isFetchImm = 1'b0;
                        isALU   = 1'b0;
                        immediate = 1'b0;
                        isCmp = 1'b0;
                        isMemSel = 1'b0;
                        isStr    = 1'b0;
                        isLd     = 1'b0;
                        isMemWrite = 1'b0;
                    end

                    DECODE: begin

                        if(ip[4:2] == 3'b000) //opcode 3'b000 (ADD and TRF)
                        begin
                            isFetchImm = 1'b0;
                            if(ip[1:0] == 2'b00) // Imm = 0 Trf = 0

                                    opcode = ip[4:2];

                            else if(ip[1:0] == 2'b01) // Imm = 0 Trf = 1

                                    {isTrf, isRegWr, isOp, isImm} = 4'b1000;

                            else if(ip[1:0] == 2'b10) // Imm = 1 Trf = 0
                            begin

                                    opcode = ip[4:2];
                                    immediate = 1;
                            end
                            else if(ip[1:0] == 2'b11) // Imm = 1 Trf = 1
                            begin

                                    {isTrf, isRegWr, isOp, isImm} = 4'b0000;
                                    immediate = 1;
                            end 
                        end

                        else if(ip[4:2] === 3'b001 || ip[4:2] === 3'b010 || ip[4:2] === 3'b011 || ip[4:2] === 3'b100 || ip[4:2] === 3'b101)  /*opcode 3'b001 (SUB) 
                                                                          opcode 3'b010 (AND)     
                                                                          opcode 3'b011 (OR)     
                                                                          opcode 3'b100 (NOT)
                                                                          opcode 3'b101 (CMP) */
                        begin 
                            if(ip[1] == 0)//Normal Sub or Normal AND or Normal OR Normal CMP
                            begin

                                    opcode = ip[4:2];
                                    if (opcode == 5)
                                        sign_flag = ip[0];
                              
                            end
                            
                            else
                            begin 
                                    opcode = ip[4:2];
                                    immediate = 1;
                                    
                            end 
                            
                        end 

                        else if(ip[4:2] == 3'b110) // opcode 3'b110 Memory (LoaD,STore)
                        begin 
                            if(ip[1] == 1)
                            begin
                                isMemSel = 1;
                                {isStr,isLd} = 2'b10;
                            end
                            else
                            begin
                                isMemSel = 1;
                                {isStr,isLd} = 2'b00; 
                            end 
                        end

                        
                    
                    end

                    FETCH_IMM: begin
                        {isTrf, isRegWr, isOp, isImm} = 4'b0000;
                        fielder = ip[1:0];
                        isFetchImm = 1'b1;
                    end

                    EXECUTE_ALU: begin
                       
                        /* EXECUTE_ALU based on several field bits we decide which control
                        signals should be triggered(based on immediate signal)
                        
                            1. If addition/sub/and/or/not/cmp is immediate then in FETCH_IMM it will store the fielder bits
                               into seperate reg named fielder

                            2. if addition/sub/and/or/not/cmp is normal then it look directly into ip[1:0]

                               */
                        if(immediate==1)
                        begin
                            if(fielder[1] == 1)
                            begin
                                {isTrf,isRegWr,isOp,isImm} = 4'b0001;
                                isALU = 1;
                                isFetchImm = 0;
                            end 
                        end

                        else
                        begin
                            if(ip[1] == 0)
                            begin
                                {isTrf,isRegWr,isOp,isImm} = 4'b0000;
                                isALU = 1;
                                isFetchImm = 0;
                            end 
                        end
                        
                    end

                    EXECUTE_MEM:
                            begin
                                if(ip[1] == 1) //Store
                                begin
                                    isMemWrite = 1;
                                    isOp       = 1;
                                end 
                                else 
                                    isLd = 1;


                            end

                    UPDATE_FLAG:
                            begin
                                isCmp = 1;
                                isOp = 1;
                            end


                    REGWRITE: begin

                        /*REGWRITE Based on several fielder bits it should trigger
                        control signals*/
                       
                        if(immediate == 1)
                        begin
                            if (fielder == 2'b11) // Imm = 1; Trf = 1
                            begin
                                {isTrf, isRegWr, isOp, isImm} = 4'b1111;
                                isFetchImm = 1'b1;
                            end

                            else if(fielder == 2'b10) // Imm = 1; Trf = 0
                            begin
                                 {isTrf, isRegWr, isOp, isImm} = 4'b0111;
                            end
                        end
                        else
                        begin
                            if(ip[0]==0) //Not a Trf 
                                {isTrf, isRegWr, isOp, isImm} = 4'b0110;
                            else if(ip[1]==0) // Memory Load
                                begin 
                                        isRegWr = 1;
                                        isOp    = 1; 
                                end
                            else
                                {isTrf, isRegWr, isOp, isImm} = 4'b1110;

                        end
    
                    end

                    default: begin
                        {isTrf, isRegWr, isOp, isImm} = 4'b0000;
                        isFetchImm = 1'b0;
                    end

                endcase
            end         
        
endmodule 