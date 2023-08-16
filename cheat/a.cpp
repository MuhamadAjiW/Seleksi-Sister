#include <iostream>
#include <windows.h>
#include <winbase.h>
#include <stdio.h>
#include <tchar.h>
#include <psapi.h>

DWORD get_pid(TCHAR* name) {
    DWORD ps_list[1024], ps_memctr, ps_ctr;
    if (!EnumProcesses(ps_list, sizeof(ps_list), &ps_memctr)) return 0;
    
    ps_ctr = ps_memctr / sizeof(DWORD);

    for (int i = 0; i < ps_ctr; i++){
        if (ps_list[i] != 0){
            TCHAR pname[MAX_PATH] = TEXT("<unknown>");
            HANDLE phandle = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, ps_list[i]);
            
            if (phandle != NULL) {
                HMODULE pmod;
                DWORD temp;
                if (EnumProcessModules(phandle, &pmod, sizeof(pmod), &temp))
                    GetModuleBaseName(phandle, pmod, pname, sizeof(pname) / sizeof(TCHAR));
            }
            // _tprintf(TEXT("%s (PID %u)\n"), pname, ps_list[i]);
            if (_tcscmp(pname, name) == 0){
                _tprintf(TEXT("%s (PID %u)\n"), pname, ps_list[i]);
                return ps_list[i];
            }
            CloseHandle(phandle);
        }
    }
    return 0;
}

void* seek_memory(DWORD pid, void* targetaddr){
    HANDLE process = OpenProcess(PROCESS_VM_READ, FALSE, pid);
    if(process != NULL){
        LPCVOID addr = (LPCVOID) targetaddr;
        char buffer[4];
        int* intptr = (int*) buffer;

        SIZE_T bytesRead;
        if (ReadProcessMemory(process, addr, buffer, sizeof(buffer), &bytesRead)){
            printf("Read %zu bytes\n", bytesRead);
            printf("Content: %d\n", *intptr);
        }
        else{
            printf("Failed to read memory with error: %u\n", GetLastError());
            printf("Content: %d\n", *intptr);
        }
        CloseHandle(process);
    }
    else{
        printf("OpenProcess failed\n");
    }
    return 0;
}

void* write_memory(DWORD pid, void* targetaddr, int newval){
    HANDLE process;
    HANDLE tprocess;

    process = OpenProcess(PROCESS_VM_OPERATION | PROCESS_VM_WRITE | PROCESS_VM_READ , FALSE, pid);

    if(process != NULL){
        LPVOID addr = (LPVOID) targetaddr;
        int buffer[1];
        buffer[0] = newval;

        int* intptr = (int*) buffer;

        SIZE_T bytesWritten;
        if (WriteProcessMemory(process, addr, buffer, sizeof(buffer), &bytesWritten)){
            printf("Written %zu bytes\n", bytesWritten);
        }
        else{
            printf("Failed to write memory with error: %u\n", GetLastError());
        }
        CloseHandle(process);
    }
    else{
        printf("OpenProcess failed\n");
    }
    return 0;
}

int main() {
    // target address ganti sesuai problemnya
    void* target_addr = (void*) 0x00000075af7ff90c;

    TCHAR* target = _T("problem.exe");
    DWORD pid = get_pid(target);
    _tprintf(TEXT("pid is: %u\n"), pid);

    if (pid != 0){
        printf("Scanning memory\n");
        seek_memory(pid, target_addr);
        write_memory(pid, target_addr, 0x00000000);
        printf("Memory after writing:\n");
        seek_memory(pid, target_addr);
    }
    
    int prompt_buf;
    std::cin >> prompt_buf;
    printf("\nDone\n");

    return 0;
}
