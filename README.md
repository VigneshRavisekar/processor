**4-bit processor**
----------------------

<img width="747" height="546" alt="image" src="https://github.com/user-attachments/assets/2d31c46c-4c7f-4109-88cc-c50dd9113958" />
                                      

<img width="580" height="255" alt="image" src="https://github.com/user-attachments/assets/c41977b6-6fe8-476b-b36c-43721f95dc6e" />

These two images form the baseline for this 4 bit microprocessor

## Detective Work 

During the implementation of the ALU and while brainstorming about Instruction Decoder, several
architectural/design issues were identified in the existing 4-bit processor.

**Design Flaw Bucket**
| # | Design Issue | Observation |
|---|---|---|
| 1 | **FETCH state / instruction fetching** | The `FETCH` state in the state diagram does not appear to fetch the instruction. Instead, it fetches data from a RAM location. The instruction-fetch mechanism therefore needs to be reconsidered. |
| 2 | **ALU → Instruction Decoder feedback loop** | The ALU generates a data output which is fed back to the Instruction Decoder as an address. For example, for `ADD 5 3`, the ALU produces `8`, which then becomes an address to the decoder. This data path does not make architectural sense for instruction execution. |
| 3 | **Insufficient / inconsistent control signals** | The ALU requires multiple select signals and a `Cin` input, while the Instruction Decoder provides a control signal which is only one bit. Attempting to use this signal to control both the ALU and memory creates an inconsistency in the control architecture. |
| 4 | **ALU registration and FSM synchronization** | Operations are executed within a state and clock cycle, but the registered ALU output does not appear to be properly synchronized with the FSM state transitions. The ALU result may therefore not be available at the point where the next state expects it. |
| 5 | **Inconsistent ALU multiplexing** | The signal selection/muxing around the ALU is inconsistent, making the intended datapath and selection of operands/results unclear. |
| 6 | **Operand 2 limitation** | Operand 2 is effectively constant, limiting the processor's ability to perform operations involving two independently selected operands, such as register-to-register operations. An attempt was made to redesign the ISA by separating the memory and ALU datapaths, but this exposed the instruction-fetch issue again. |
                                      
## Proposed Design Changes

Working on finding even more interesting design flaws (hoping to add more as a
Verif Engineer in the design flaw bucket) and then improvising the design
changes.

**WORK IN PROGRESS**

The first step is completely redesigning the architecture, like generating a custom Instruction Set Architecture, where moving the 4-bit processor to an 8-bit processor to support branching, memory operations, and also to address the limitations faced in a 4-bit processor. 

### Instruction Set Architecture 

This is the proposed ISA compact one which can handle 18 instructions with each instruction occupying 8 bits and subdivided into arithmetic/logical, compare, memory and branching instructions. Several instructions share same opcode with several field bits distinguishing the instructions. Attaching the ISA document.
# Custom 8-bit Processor — ISA Quick Reference

## Register File

| Register | Use |
| --- | --- |
| X0–X6 | General-purpose registers |
| X7 | Accumulator / default register |

## Opcode Map

| Opcode | Instruction(s) | Category |
| --- | --- | --- |
| `000` | ADD / TRF | Arithmetic / Transfer |
| `001` | SUB | Arithmetic |
| `010` | AND | Logical |
| `011` | OR | Logical |
| `100` | NOT | Logical |
| `101` | CMP | Compare |
| `110` | LD / ST | Memory |
| `111` | B / BEQ / BGT | Branching |

## 1. Arithmetic / Logical / Transfer

| Opcode | imm | trf / R-field | R-field / Source register | Instruction | Operation |
| --- | --- | --- | --- | --- | --- |
| `000` | 0 | 0 | Xn | `ADD Xn` | `X7 ← X7 + Xn` |
| `000` | 0 | 1 | Xn | `TRF Xn` | `Xn ← X7` |
| `000` | 1 | 0 | reserved | `ADD #imm` | `X7 ← X7 + imm` |
| `000` | 1 | 1 | reserved | `TRF #imm` | `X7 ← imm` |
| `001` | 0 | 0 | Xn | `SUB Xn` | `X7 ← X7 − Xn` |
| `001` | 1 | 0 | reserved | `SUB #imm` | `X7 ← X7 − imm` |
| `010` | 0 | reserved | Xn | `AND Xn` | `X7 ← X7 AND Xn` |
| `010` | 1 |  | reserved | `AND #imm` | `X7 ← X7 AND imm` |
| `011` | 0 |  | Xn | `OR Xn` | `X7 ← X7 OR Xn` |
| `011` | 1 |  | reserved | `OR #imm` | `X7 ← X7 OR imm` |
| `100` | 0 |  | Xn | `NOT` | `X7 ← NOT Xn` |

> **Immediate-form note:** `imm = 1` selects the immediate form; immediate instructions require an additional byte.

## 2. Compare Operations

| Opcode | IMM | U/S | Source register / R-field | Instruction | Operation |
| --- | --- | --- | --- | --- | --- |
| `101` | 0 | 0 = Unsigned<br>1 = Signed | Xn | `CMP Xn` | Internally subtract `X7 − Xn`; update EQ and GT flags only. X7 is not written. |
| `101` | 1 | 0 = Unsigned<br>1 = Signed | Reserved | `CMP #imm` | Internally subtract `X7 − imm`; update EQ and GT flags only. X7 is not written. Immediate occupies the next byte. |

> **CMP note:** EQ indicates equality. GT is calculated using the selected signed/unsigned interpretation. The subtraction result is not written back to X7.
>
> **Immediate-form note:** `imm = 1` selects the immediate form; immediate instructions require an additional byte.

## 3. Memory Operations

| Opcode | LD/ST | R-field | Source register | Instruction | Operation |
| --- | --- | --- | --- | --- | --- |
| `110` | 0 = Load | Reserved | Xn | `LD [Xn]` | `X7 ← DataMem[Xn]` |
| `110` | 1 = Store | Reserved | Xn | `ST [Xn]` | `DataMem[Xn] ← X7` |

> **Memory note:** LD/ST shares opcode `110`; the LD/ST bit selects the direction. The memory address is taken from Xn.

## 4. Branching Operations

| Opcode | UC | E | Source register | Assembly | Meaning |
| --- | --- | --- | --- | --- | --- |
| `111` | 1 | \_ | Xn | `b loop` | Unconditional branch |
| `111` | 0 | 1 | Xn | `beq loop` | Conditional branch: equal |
| `111` | 0 | 0 | Xn | `bgt loop` | Conditional branch: greater-than |


