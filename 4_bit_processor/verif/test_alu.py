import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import Timer,RisingEdge,FallingEdge
from cocotb.types import LogicArray,Range
import logging

log = logging.getLogger("cocotb")


def comparsion_block(output,op_code,dut_out,dut_cout):

           
            if op_code == 0 or op_code == 7:

                  tb_out  = int(output)
                  print(f"ALU_OUTPUT:{int(dut_out)} || TB_OUTPUT:{tb_out}")
                  if tb_out == dut_out:
                              log.info("COMPARISON PASSED!!!")
                  else:
                              log.error("COMPARISON FAILED!!!")

            elif op_code >= 1 and op_code <7:

                  tb_out = int(output[3:0])
                  tb_cout = int(output[4])
                  print(f"ALU_OUTPUT:{int(dut_out)} || TB_OUTPUT:{tb_out} *** ALU_COUT: {dut_cout} || TB_COUT: {tb_cout} ")
                  if tb_out == dut_out and tb_cout == dut_cout :
                        log.info("COMPARISON PASSED!!!")
                  else:
                        log.error("COMPARISON FAILED!!!")

            else:
                  
                   print(f"ALU_OUTPUT:{int(dut_out)} || TB_OUTPUT:{int(output)}")
                   if output == dut_out:
                                log.info("COMPARISON PASSED!!!")
                   else:
                                log.error("COMPARISON FAILED!!!")
      



def arithmetic_block(in_1,in_2,select,cin,cout):

        print(select,cin)   
        opcode = int(str(select) + str(cin),2)
        print(f"OPCODE:{opcode}")     
        if opcode == 0 or opcode == 7:

              f = in_1
     
        elif opcode == 1:
              
              f = LogicArray(int(in_1) + 1,5)

                
        elif opcode == 2:
              
                f = LogicArray(int(in_1) + int(in_2),5)
           
                  
        elif opcode == 3:

              f = LogicArray(int(in_1) + int(in_2) + 1,5)
          
        elif opcode == 4:

              f  = LogicArray(int(in_1) + int(~in_2),5)
         
             
        elif opcode == 5:

              f = LogicArray(int(in_1) + int(~(in_2)) + 1 ,5)
          
        elif opcode == 6:
              
              f = LogicArray(int(in_1) + 15,5) # -1 is reprsented as 15 
     
        else:
              log.error("INCORRECT OPCODE")
              

        return f

def logical_block(in_1,in_2,select):
        
        print(f"OPCODE:{int(select)}")
        if int(select) == 4:
              
              f = in_1 | in_2
             
      
        elif int(select) == 5:
              
              f = in_1 ^ in_2
     
        elif int(select) == 6:
              
              f = in_1 & in_2
     
        elif int(select) == 7:
              
              f =  ~ in_1
             
        else:
              log.error("INCORRECT OPCODE")

        return f
              


class alu_base:

    def __init__(self,dut):

        self.a = dut.a
        self.b = dut.b
        self.select = dut.select
        self.cin  = dut.cin
        self.clk  = dut.clk
        self.rst_n = dut.rst_n
        self.cout  = dut.cout
        self.f = dut.f

    async def selector(self):

            await Timer(1,"ns")
            if int(self.select.value) < 4:

                
                 result = arithmetic_block(self.a.value,self.b.value,self.select.value,self.cin.value,self.cout.value)

            else:

                 result = logical_block(self.a.value,self.b.value,self.select.value)
                 print(result)

            return result
                
         
         
    
    
@cocotb.test()
async def test_arithmetic_operation(dut):

    alu = alu_base(dut)
    cocotb.start_soon(Clock(alu.clk,1,"ns").start())
    alu.rst_n.value = 0
    await Timer(2,"ns")
    alu.rst_n.value = 1
    for _ in range(10):
        alu.select.value = random.randint(0,3)
        alu.a.value = random.randint(0,15)
        alu.b.value = random.randint(0,15)
        alu.cin.value = random.randint(0,1)
        await Timer(1,"ns")
        print(f"A_VALUE:{int(alu.a.value)}")
        print(f"B_VALUE:{int(alu.b.value)}")
        print(f"CIN_VALUE:{alu.cin.value}")
        print(f"SELECT_VALUE:{int(alu.select.value)}")
        opcode = int(str(alu.select.value) + str(alu.cin.value),2)
        output = await alu.selector()
        comparsion_block(output,opcode,alu.f.value,alu.cout.value)

@cocotb.test()
async def test_logical_operation(dut):

         alu = alu_base(dut)
         cocotb.start_soon(Clock(alu.clk,1,"ns").start())
         alu.rst_n.value = 0
         await Timer(2,"ns")
         alu.rst_n.value = 1
         for _ in range(10):
             alu.select.value = random.randint(4,7)
             alu.a.value = random.randint(0,15)
             alu.b.value = random.randint(0,15)
             alu.cin.value = random.randint(0,1)
             await Timer(1,"ns")
             print(f"A_VALUE:{int(alu.a.value)}")
             print(f"B_VALUE:{int(alu.b.value)}")
             print(f"CIN_VALUE:{alu.cin.value}")
             print(f"SELECT_VALUE:{int(alu.select.value)}")
             opcode = int(str(alu.select.value) + str(alu.cin.value),2)
             output = await alu.selector()
             comparsion_block(output,opcode,alu.f.value,alu.cout.value)




     


     

