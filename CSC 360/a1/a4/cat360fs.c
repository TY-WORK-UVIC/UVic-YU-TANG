#include <assert.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <string.h>
#include "disk.h"
int counter=0;
int counter_Free=0;
int counter_Resv=0;
int counter_Alloc=0;


int dir_start;  
int dir_blocks;
int Bsz;
int start_block;
int num_blocks;
int file_size;

short a[2];  // Variables for unpack_datetime
short b[2];
short c[2];
short d[2];
short e[2];
short f[2];

int file_counter=0;

void unpack_datetime(unsigned char *time, short *year, short *month, 
    short *day, short *hour, short *minute, short *second)
{
   
    assert(time != NULL);

    memcpy(year, time, 2);   
    *year = htons(*year);
    *month = (unsigned short)(time[2]);   
    *day = (unsigned short)(time[3]);
    *hour = (unsigned short)(time[4]);
    *minute = (unsigned short)(time[5]);
    *second = (unsigned short)(time[6]);
}
char *month_to_string(short m) {
    switch(m) {
    case 1: return "Jan";
    case 2: return "Feb";
    case 3: return "Mar";
    case 4: return "Apr";
    case 5: return "May";
    case 6: return "Jun";
    case 7: return "Jul";
    case 8: return "Aug";
    case 9: return "Sep";
    case 10: return "Oct";
    case 11: return "Nov";
    case 12: return "Dec";
    default: return "?!?";
    }
}

void open_file1(char *imagename,superblock_entry_t sb){  // Find blocksize, block where root directory starts, and # of blocks in root directory
     FILE  *f;
    FILE  *f11;

   f=fopen(imagename,"rb");  
   fread(&sb, sizeof(sb), 1, f);
   dir_start=ntohl(sb.dir_start); // block where root directory starts
   dir_blocks= ntohl(sb.dir_blocks); // # of blocks in root directory
   Bsz=ntohs(sb.block_size);  // blocksize
    fclose(f);
   f11=fopen(imagename,"rb");
 
   fseek( f11, 256, SEEK_SET ); // jump to FAT
   int numberArray[ntohl(sb.num_blocks)];
   int i;

   fread(numberArray, sizeof(numberArray), 1, f11); // Find  free, reserved ,allocated  blocks
   for (i = 0; i <= ntohl(sb.num_blocks); i++){
         if(ntohl(numberArray[i])==0x00000000){
           counter_Free+=1;
           
       }
       if(ntohl(numberArray[i])==0x00000001){
            counter_Resv+=1;
        }
        if((0x00000002<ntohl(numberArray[i])) & (ntohl(numberArray[i])<=0xffffff00)){
            counter_Alloc+=1;
        }
      
   }  
  
    fclose(f11);
}

void open_file(char *imagename, char* filename){
   FILE  *f1;
   f1=fopen(imagename,"rb");
   directory_entry_t de; 
 
    int total=(dir_blocks*Bsz)/64; // Total directory entries
 
    while(counter<total){ // Make sure read all the entries
         fseek( f1, dir_start*Bsz+(64*counter), SEEK_SET );  // jump to each entries
         fread(&de, sizeof(de), 1, f1);
        if(de.status!=0){  // If there is value, print it out 
                   
            if(strcmp(filename,de.filename)==0){ // Find the filenames so the file exist
                start_block=ntohl(de.start_block); // Store all the needed data
                num_blocks=ntohl(de.num_blocks);
                file_size=ntohl(de.file_size);
                file_counter++;
                break;                           // End the loop
            }    
        
        }
         counter++;
    }
           
    fclose(f1);
}

void open_file2(char * imagename,char * filename){
    FILE *f;
 
    char buffer[file_size+1];
    f=fopen(imagename,"rb");
    if(file_counter==0){ // If file does not exist, quit 
        exit(1);
    }
    fseek( f, start_block*Bsz, SEEK_SET ); // Go the block where root directory starts
    
    fread(buffer, sizeof(buffer), 1, f); // Store the data into a char array size 
    printf("%s\n", buffer);
   
}

void file_and_image(char * imagename,char * filename){
    printf("imagename %s\n", imagename);
    printf("filename %s\n", filename);
}
int main(int argc, char *argv[]) {
    superblock_entry_t sb;
    int  i;
    char *imagename = NULL;
    char *filename  = NULL;
   

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--image") == 0 && i+1 < argc) {
            imagename = argv[i+1];
            i++;
        } else if (strcmp(argv[i], "--file") == 0 && i+1 < argc) {
            filename = argv[i+1];
            i++;
        }
    }
     
    if (imagename == NULL || filename == NULL) {
        fprintf(stderr, "usage: cat360fs --image <imagename> " \
            "--file <filename in image>");
        exit(1);
    }
    open_file1(imagename,sb);
    open_file(imagename,filename);
    
    open_file2(imagename,filename);
    return 0; 
}
