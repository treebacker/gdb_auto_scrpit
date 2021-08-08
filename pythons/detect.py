import idc
import idaapi
import idautils
import os


# Run in IDAPro 7.5
# idat -A -S"detect.py" in_file
def is_ret(addr):
    asm = GetDisasm(addr)
    return ("ret" in asm)



def is_call(addr):
    asm = GetDisasm(addr)
    return ("call" in asm)


def is_call_exec(addr):
    asm = GetDisasm(addr)

    pass

def find_all_getuid():
    getuid_funcs = []
    code_start = None
    code_end = None
    call_getuid_addrs = []
    # find all getuid functions
    for seg_ea in Segments():
        seg_name = get_segm_name(seg_ea)
        if "text" in seg_name:
            code_start = get_segm_start(seg_ea)
            code_end = get_segm_end(seg_ea)
            print("code_start: {}; code_end: {}".format(hex(code_start), hex(code_end)))
        for function_ea in Functions(seg_ea, get_segm_end(seg_ea)):
            if(get_func_name(function_ea)).endswith("getuid"):
                print("getuid: ", function_ea)
                getuid_funcs.append(function_ea)


    for getuid_addr in getuid_funcs:
        refs = CodeRefsTo(getuid_addr, 0)            # where calls afl_maybe_log
        for ref_addr in refs:
            if (ref_addr < code_start) or (ref_addr > code_end) :
                continue
            print("call getuid address: {}".format(hex(ref_addr)))
            call_getuid_addrs.append(ref_addr)

    return call_getuid_addrs


def ends_constains(array, name):
    for i in array:
        if name.endswith(i):
            return True
    return False

def is_exec_shell(addr):
    exec_funcs = ["system", "execl", "execve"]
    # search call exec_funcs
    inst = next_head(addr)
    while not is_ret(inst):
        if is_call(inst):
            target_addr = [x for x in CodeRefsFrom(inst, 0)][0]
            name = get_func_name(target_addr)

            if ends_constains(exec_funcs, name):
                return True
        inst = next_head(inst)

    return False

def follow_addr(addr):
    sh = False
    inst = next_head(addr)
    # if getuid == 0
    if print_insn_mnem(inst) == "test":
        last = next_head(inst)
        if print_insn_mnem(last) == "jz":
            target_addr = [x for x in CodeRefsFrom(last, 0)][0]

            sh = is_exec_shell(target_addr)
            print("check address: {}".format(hex(target_addr)))
            pass
        elif print_insn_mnem(last) == "jnz":
            next_addr = [x for x in CodeRefsFrom(last, 1)][0]
            sh = is_exec_shell(next_addr)
            print("check address: {}".format(hex(next_addr)))
            pass

    return sh


def write_logs(log):
    with open("F:\\sandbox\\lpe_samples\\logs.txt", 'w') as f:
        f.write(log)

if __name__ == '__main__':
    auto_wait()
    call_addrs = find_all_getuid()
    for i in call_addrs:
        ret = follow_addr(i)
        if ret:
            write_logs(hex(i))
            print("spawn root shell at: {}".format(hex(i)))
    idc.exit()
