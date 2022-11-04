/* getstats.c 
 *
 * CSC 360, Summer 2022
 *
 * - If run without an argument, dumps information about the PC to STDOUT.
 *
 * - If run with a process number created by the current user, 
 *   dumps information about that process to STDOUT.
 *
 * Please change the following before submission:
 *
 * Author: Luke Skywalker
 * Login:  usetheforce@uvic.ca 
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <stdbool.h>
/*
 * Note: You are permitted, and even encouraged, to add other
 * support functions in order to reduce duplication of code, or
 * to increase the clarity of your solution, or both.
 */
void delete_space(char * line){ //Delete the space at end of each line 
    int index= -1;
    int i = 0;
    while(line[i] != '\0'){
        if(line[i] != '\t' && line[i] != '\n' &&line[i] != ' ' ){ //check if it is the end of line 
            index= i;
        }
        i+=1;
    }
    index= index+1;
    line[index] = '\0'; // Delete the space at the end of line 
}


void No_numerical(char* name_of_file, char* name ){ // Print out the info when there is no numerical
     char filename[50];
    sprintf(filename, "/proc/%s", name_of_file);
    FILE *fd=fopen(filename,"r");
    char line[1000];
  
    char* token;
    int counter=0;
    int done=0;
    while(fgets(line,sizeof(line),fd)!=NULL){      
        if(done==1){
            break;
        }
        token = strtok(line,":"); // Use strtok to find the info we need which is after ": "
        delete_space(token);    // Delete space of each line. 
        while(token !=NULL){
          
            if(counter ==1){
               counter=2;
               printf("%s   : %s", name, token); // Print out the info we need 
               done +=1;  
               break;
            }
            if(strcmp(token, name)==0){
                counter +=1;
            }
          token=strtok(NULL,":");  
        }
    }
  
    fclose(fd); // Close the directory 
}    

void print_out_version(char* path){ // Print out version
    char filename[50];
    char line[1000];
    sprintf(filename, "/proc/%s", path); // Create the path 
    FILE *fd=fopen(filename,"r");
    while(fgets(line,sizeof(line),fd)!=NULL){
         printf("%s", line);
    }
    fclose(fd);
}
void print_out_uptime(char* path){ // Count the uptime
    char filename[50];
    char line[1000];
    char* token;
    sprintf(filename, "/proc/%s", path);
    FILE *fd=fopen(filename,"r");
    while(fgets(line,sizeof(line),fd)!=NULL){
        token = strtok(line," ");
        int seconds= atoi(token);
        int days = seconds/3600/24; // Count days
        int hours=(seconds- days*3600*24)/3600; // Count hours 
        int minutes= (seconds- days*24*3600- hours*3600)/60; // Count minutes
        int remainder=(seconds- days*24*3600- hours*3600-minutes*60); // Count seconds 
        printf("Uptime: %d days , %d hours, %d minutes, %d seconds\n", days,hours,minutes,remainder); // Print the uptime 
        
    }
    fclose(fd);
}
    
void print_with_numerical(char* name, char* path){ // Print the info when there is a number on command line 
    char filename[50];
    char line[1000];
    sprintf(filename, "/proc/%s/status", path);  // Create the path 
    FILE *fd=fopen(filename,"r");
    if(fd ==NULL){
        printf("Process number %s not found.",path); // Print the message when path not exist 
    }
    char* token;
    int counter=0;
    int done=0;
    while(fgets(line,sizeof(line),fd)!=NULL){      
        if(done==1){
            break;
        }
        token = strtok(line,":");       // Seperate the line with ":"
        delete_space(token);       
        while(token !=NULL){
            
            if(counter ==1){
               counter=2;
               
               printf("%s   : %s", name, token); // Print the info 
               done +=1;  
               break;
            }
            if(strcmp(token, name)==0){                         
                counter +=1;
                   
            }
          token=strtok(NULL,":");  
        }
    }
    fclose(fd); // Close the file 
}
void print_out_filename(char* path1, char* path2){ // Print out the filename
    char filename[50];
    char line[1000];
    sprintf(filename, "/proc/%s/%s", path1, path2); // It uses different path 
    FILE *fd=fopen(filename,"r");
    while(fgets(line,sizeof(line),fd)!=NULL){
        printf("Filename (if any) : %s", line); // Print the info out. 
    }
    fclose(fd);
}

int print_out_Total_context_switches(char*path, char* name1){ // Find the number of context 
    char filename[50];
    char line[1000];
    sprintf(filename, "/proc/%s/status", path); // Create the path 
    FILE *fd=fopen(filename,"r");
    char* token;
    int counter=0;
    int done=0;
    int result=0;
    while(fgets(line,sizeof(line),fd)!=NULL){
        
        if(done==1){
            break;
        }
        token = strtok(line,":");
        delete_space(token);
        
        while(token !=NULL){     
           if(counter ==1){
               counter=2;
               
               result=atoi(token); // Transforme the char into the integer 
               done +=1;  
               break;
            }
            if(strcmp(token, name1)==0){             
                counter =1;   
            }
          token=strtok(NULL,":");  
        }
    }
    fclose(fd);
    return result; // Return the number of context_switches
}
int check_if_exist(char * process_num) { // Check if this directory is exist
    char filename[50];
    
    sprintf(filename, "/proc/%s/status", process_num); // Create the path 
    FILE *fd=fopen(filename,"r");
    int result=0;
    
    if(fd ==NULL){
        result=-1;
        printf("Process 1s number %s not found.\n", process_num); // If the path not exist, print the message
        
    }
    
    return result;
}
void print_process_info(char * process_num) { // Print out if there is a number 
    int check =check_if_exist(process_num);  // Check if this directory is exist 
    if(check ==-1){     // If not , exit 
        
        exit(1);
    }
    printf("Process number: %s\n", process_num); // Print out all the info that we need include, Process number, Name etc
    char* a="Name";
    char *b=process_num;
    print_with_numerical(a,b);
    
    char* d="comm";
    print_out_filename(process_num,d);
    
    char* c="Threads";
    print_with_numerical(c,b);
    
    char *e="voluntary_ctxt_switches";
    char *f="nonvoluntary_ctxt_switches";
    int result=print_out_Total_context_switches(process_num,e); 
    int result2=print_out_Total_context_switches(process_num,f);
    int final=result+result2;   // Find voluntary_ctxt_switches and nonvoluntary_ctxt_switches, then sum them. 
   
    printf("Total context switches: %d \n",final); // Print the sum 
} 


void print_full_info() { // Print the info when no numerical
    
    char* a ="model name"; // Input the name of info
    char* b= "cpuinfo";   // Path of this info
    No_numerical(b,a);
    
    char* c ="cpu cores"; // Input the name of info
    char* d= "cpuinfo";   // Path of this info
    No_numerical(d,c);
    
    char* e= "version";
    print_out_version(e);  //  Print_out_version
    
    char* f= "MemTotal";
    char* g= "meminfo";
    No_numerical(g,f);
    
    char* h= "uptime";
    print_out_uptime(h);
   
}


    
int main(int argc, char ** argv) {  
    if (argc == 1) {
        print_full_info();
    } else {
        print_process_info(argv[1]);
    }
}
