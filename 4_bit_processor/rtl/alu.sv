module alu(input logic [3:0] a,b,input logic [2:0] select,input logic cin,input clk,rst_n,output logic [3:0] f, output logic cout);

                // inner signals
                logic [3:0] b_sel,f_arth,f_logic;
                logic [3:0] u_f;
                logic  u_cout;
                logic cin_sel;
        
                always_comb begin

                        if(({select,cin}==1))
                                cin_sel = 0;
                        else
                                cin_sel = cin;
                end



                always_comb begin

                        b_sel   = 0;
                        f_logic = 0;


                        case({select,cin}) inside 

                                4'b0000:

                                       b_sel = 0;

                                4'b0001:

                                       
                                        b_sel = 1;
                                
                                       

                                4'b0010, 4'b0011:

                                       b_sel = b;
                             

                                4'b0100, 4'b0101:

                                       b_sel = ~b;

                                4'b0110:

                                       b_sel = -1;
                                
                                4'b0111:

                                       b_sel = 15;
                                
                                4'b100?:

                                       f_logic = a | b;
                                
                                4'b101?:

                                       f_logic = a ^ b;
                                
                                4'b110?:

                                       f_logic = a & b;

                                4'b111?:

                                       f_logic = ~a;


                        endcase
                end
                
                top_adder adder(.a(a),.b(b_sel),.cin(cin_sel),.sum(f_arth),.cout(u_cout));


                assign u_f = (select>3)? f_logic : f_arth ;

                always_ff@(posedge clk or negedge rst_n)
                begin
                        if(rst_n==0)
                        begin
                                f <= 0;
                                cout <= 0;
                        end
                        else
                        begin
                                f<=u_f;
                                cout<=u_cout;
                        end
                end



endmodule