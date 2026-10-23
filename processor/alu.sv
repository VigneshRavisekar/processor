module alu(input logic [7:0] op1,op2,input logic [2:0] opcode, output logic [7:0] alu_result);


            always_comb begin

                        case(opcode)

                            3'b000: alu_result = op1 + op2;

                            default: alu_result = 0;

                        endcase
            end


endmodule 