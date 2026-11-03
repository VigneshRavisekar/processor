SIM ?= icarus 
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES +=  *.sv

TOPLEVEL = processor
MODULE = test_cpu


WAVES = 1


include $(shell cocotb-config --makefiles)/Makefile.sim

# SIM ?= verilator
# EXTRA_ARGS += --trace --trace-structs --fourstate --timing  Wno-LATCH   
# TOPLEVEL_LANG ?= verilog
# VERILOG_SOURCES += *.sv
# TOPLEVEL = processor
# MODULE = test_cpu


# include $(shell cocotb-config --makefiles)/Makefile.sim
