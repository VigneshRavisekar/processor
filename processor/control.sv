module control(input logic clk,rstn, input logic [4:0] ip, output logic [2:0] opcode, output logic isTrf,isRegWr,isOp,isFetchImm,isImm,isALU);

            

            typedef enum logic [3:0] {RESET = 0, FETCH = 1, DECODE = 2, FETCH_IMM = 3, EXECUTE_ALU = 4, REGWRITE = 5} states_t;
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
                                                immediate = 1;
                                            end
                                    end


                                else // Addition bit selected

                                    begin 

                                        if(ip[1] == 0) // Normal Addition
                                                next_state = EXECUTE_ALU;
                                        
                                        else 
                                            begin
                                                next_state = FETCH_IMM;
                                                immediate = 1;
                                            end 
                                    end 

                            end

                            else 

                                    next_state = DECODE;
                            
                        end

                    EXECUTE_ALU:

                                next_state = REGWRITE;
                
                    FETCH_IMM:
                    begin 
                            /* OPCODE 000 in Fetch_Imm to indicate Trf/Add Instruction
                            trf bit tell next_state*/
                            if(ip[4:2]==0) 
                            begin
                                if(ip[0] == 0)
                                    next_state = EXECUTE_ALU;
                                else
                                    next_state = REGWRITE;
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
                    end

                    DECODE: begin

                        if(ip[4:2] == 3'b000) //opcode 3'b000 
                        begin
                            isFetchImm = 1'b0;
                            if(ip[1:0] == 2'b00) // Imm = 0 Trf = 0

                                    opcode = ip[4:2];

                            else if(ip[1:0] == 2'b01) // Imm = 0 Trf = 1

                                    {isTrf, isRegWr, isOp, isImm} = 4'b1000;

                            else if(ip[1:0] == 2'b10) // Imm = 1 Trf = 0

                                    opcode = ip[4:2];

                            else if(ip[1:0] == 2'b11) // Imm = 1 Trf = 1

                                    {isTrf, isRegWr, isOp, isImm} = 4'b0000;

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
                        
                            1. If addition is immediate then in FETCH_IMM it will store the fielder bits
                               into seperate reg named fielder

                            2. if addition is normal then it look directly into ip[1:0]

                               */
                        if(immediate==1)
                        begin
                            if(fielder == 2)
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

                    REGWRITE: begin

                        /*REGWRITE Based on several fielder bits it should trigger
                        control signals*/
                       
                        if(immediate == 1)
                        begin
                            if (fielder == 2'b11) // Imm = 1; Trf = 0
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
                                {isTrf, isRegWr, isOp, isImm} = 4'b0111;
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