import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import Timer,RisingEdge,FallingEdge,ReadOnly
from cocotb.handle import Force,Release
from cocotb.types import LogicArray
import logging

log = logging.getLogger("cocotb")

@cocotb.test()
async def test_write_read(dut):

           
            cocotb.start_soon(Clock(dut.clk,1,"ns").start())
            dut.rst_n.value = 0
            dut.csn.value = 1
            await Timer(3,"ns")
            dut.rst_n.value = 1
            dut.csn.value = 0
            ## Memory Write Operation
            dut.rwn.value = 0
            for address in range(16):
                await RisingEdge(dut.clk)
                dut.addr.value = address
                dut.data.value = random.randint(0,15)
                await Timer(0.5,"ns") 
                log.info(f"Address: {dut.addr.value} WRITE_Data:{dut.data.value}")
            dut.data.value = "ZZZZ"
            await Timer(4,"ns")
            dut.rwn.value = 1
            for address in range(15,0,-1):
                            await RisingEdge(dut.clk)
                            dut.addr.value = address
    

          
            await Timer(100,"ns")