#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <string.h>
#include "disk.h"

#include <byteswap.h>

int counter=0;        // Counters for free, reserved ,allocated  blocks
int counter_Free=0;
int counter_Resv=0;
int counter_Alloc=0;
void open_file(char *imagename,superblock_entry_t sb){
     FILE  *f;
    FILE  *f1;


    f=fopen(imagename,"rb");
    printf("360fs (%s) \n", imagename); // Print the file name 

   fread(&sb, sizeof(sb), 1, f);   // Read the file to the struct 
    
   printf ( "Bsz   Bcnt  FATst FATcnt  DIRst DIRcnt \n");    // Print out the info
   printf(  "%d    %d    %d   %d    %d    %d \n", ntohs(sb.block_size),ntohl(sb.num_blocks),ntohl(sb.fat_start),ntohl(sb.fat_blocks),ntohl(sb.dir_start),ntohl(sb.dir_blocks));
          
   
   
   fclose(f);
   f1=fopen(imagename,"rb");
   directory_entry_t de; 
   fseek( f1, 256, SEEK_SET );     // Jump to next block which is 256 bytes
   int numberArray[ntohl(sb.num_blocks)];
   int i;

   fread(numberArray, sizeof(numberArray), 1, f1);
   for (i = 0; i <= ntohl(sb.num_blocks); i++){ // check the value of each block 

       
         if(ntohl(numberArray[i])==0x00000000){ // Count free blocks
           counter_Free+=1;
           
       }
       if(ntohl(numberArray[i])==0x00000001){ // Count  reserved blocks
            counter_Resv+=1;
        }
        if((0x00000002<ntohl(numberArray[i])) & (ntohl(numberArray[i])<=0xffffff00)){ // Count allocated blocks
            counter_Alloc+=1;
        }
      
   }
   printf ( "Free   Resv  Alloc \n");  // Print them out 
   printf(  "%d    %d    %d \n",  counter_Free,counter_Resv,ntohl(sb.num_blocks)-(counter_Free+counter_Resv));
   
   fclose(f1);
}
int main(int argc, char *argv[]) {
    superblock_entry_t sb;
    int  i;
    char *imagename = NULL;
    FILE  *f;
    int   *fat_data;

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--image") == 0 && i+1 < argc) {
            imagename = argv[i+1];
            i++;
        }
    }
 
   
    if (imagename == NULL)
    {
        fprintf(stderr, "usage: stat360fs --image <imagename>\n");
        exit(1);
    }
    open_file(imagename,sb);
    return 0; 
}
