module cpu(input logic clk,rstn,input logic [7:0] instr,input logic [15:0] pc, output logic [15:0] next_pc);

                
                logic [2:0] reg_w_addr;
                logic [7:0] reg_w_data;
                logic [7:0] reg_r_data1,reg_r_data2;
                logic isTrf,isRegWr,isOp,isFetchImm,isImm,isALU;
                logic [1:0] addr_select, data_select;
                logic [15:0] temp_pc;
                logic [2:0] opcode;
                logic [7:0] op1,op2,alu_result;
                logic [7:0] w_dat_1;

             

    
    
                
                reg_file register(.RA1(3'b111),.RA2(instr[2:0]),.WA(reg_w_addr),.WD(reg_w_data),.WE(isRegWr),.clk(clk),.RD1(reg_r_data1),.RD2(reg_r_data2));
                control  control(.clk(clk),.rstn(rstn),.ip(instr[7:3]),.opcode(opcode),.isTrf(isTrf),.isRegWr(isRegWr),.isOp(isOp),.isFetchImm(isFetchImm),.isImm(isImm),.isALU(isALU)); 
                alu      alu(.op1(op1),.op2(op2),.opcode(opcode),.alu_result(alu_result));
               
                     
                assign next_pc = temp_pc;



                //READ_DATA_PATH_1
                assign op1 = reg_r_data1;
                //READ_DATA_PATH_2
                assign op2 = (isImm)? instr[7:0] : reg_r_data2;


                

                always_comb begin

                      // WRITEBACK_ADDRESS_MUX_PATH
                    addr_select = {isTrf,isImm};
                    case(addr_select)

                            2'b00,2'b01,2'b11: reg_w_addr = 3'b111; 
                            2'b10: reg_w_addr = instr[2:0];
                            default: reg_w_addr = 3'bx;
                    endcase
                    //WRITEBACK_DATA_MUX PATH
                    data_select = {isTrf,isImm};
                    case(data_select)

                            // 2'b00,2'b01,2'b11: reg_w_data = 0;
                            2'b10: w_dat_1 = reg_r_data1;
                            2'b11: w_dat_1 = instr[7:0];
                            default: w_dat_1 = 8'bx;
                    endcase
                    
                            
                end
                
                always_latch begin 

                        if(isALU)
                                reg_w_data <= alu_result;
                        else
                                reg_w_data <= w_dat_1;
                end
                
                assign temp_pc = (isFetchImm) ? pc + 16'd1 : (isOp) ? pc + 16'd1 : pc;
                
          

endmodule