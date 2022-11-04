#include <arpa/inet.h>
#include <assert.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include "disk.h"


/*
 * Based on http://bit.ly/2vniWNb
 */
int counter=0;
int counter_Free=0;
int counter_Resv=0;
int counter_Alloc=0;

int dir_start;
int dir_blocks;
int Bsz;

short a[2];    // Variables for unpack_datetime
short b[2];
short c[2];
short d[2];
short e[2];
short f[2];


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

void open_file1(char *imagename,superblock_entry_t sb){ // Find blocksize, block where root directory starts, and # of blocks in root directory
     FILE  *f;
    f=fopen(imagename,"rb");
    printf("imagename %s\n" ,imagename); 
   fread(&sb, sizeof(sb), 1, f);
    printf("imagename %s\n" ,imagename); 
   dir_start=ntohl(sb.dir_start); // block where root directory starts
   dir_blocks= ntohl(sb.dir_blocks); // # of blocks in root directory
   Bsz=ntohs(sb.block_size);  // blocksize
   
   fclose(f);
}
void open_file(char *imagename){
   FILE  *f1;
   f1=fopen(imagename,"rb");
   directory_entry_t de; 
 
   int total=(dir_blocks*Bsz)/64; // Total directory entries
 
    while(counter<total){ // Make sure read all the entries
         fseek( f1, dir_start*Bsz+(64*counter), SEEK_SET ); // jump to each entries
         fread(&de, sizeof(de), 1, f1);
        if(de.status!=0){ // If there is value, print it out 
            
            unpack_datetime(de.create_time,a,b,c,d,e,f);
            printf("%d %d-%s-%d %d:%d:%d %s\n", ntohl(de.file_size), *a,month_to_string(*b),*c,*d,*e,*f,de.filename);
        
        }
         counter++;
    }
              
    fclose(f1);
}
void pack_current_datetime(unsigned char *entry) {
    assert(entry);

    time_t t = time(NULL);
    struct tm tm = *localtime(&t);

    unsigned short year   = tm.tm_year + 1900;
    unsigned char  month  = (unsigned char)(tm.tm_mon + 1);
    unsigned char  day    = (unsigned char)(tm.tm_mday);
    unsigned char  hour   = (unsigned char)(tm.tm_hour);
    unsigned char  minute = (unsigned char)(tm.tm_min);
    unsigned char  second = (unsigned char)(tm.tm_sec);

    year = htons(year);

    memcpy(entry, &year, 2);
    entry[2] = month;
    entry[3] = day;
    entry[4] = hour;
    entry[5] = minute;
    entry[6] = second; 
}


int next_free_block(int *FAT, int max_blocks) {
    assert(FAT != NULL);

    int i;

    for (i = 0; i < max_blocks; i++) {
        if (FAT[i] == FAT_AVAILABLE) {
            return i;
        }
    }

    return -1;
}


int main(int argc, char *argv[]) {
    superblock_entry_t sb;
    int  i;
    char *imagename  = NULL;
    char *filename   = NULL;
    char *sourcename = NULL;
    FILE *f;

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--image") == 0 && i+1 < argc) {
            imagename = argv[i+1];
            i++;
        } else if (strcmp(argv[i], "--file") == 0 && i+1 < argc) {
            filename = argv[i+1];
            i++;
        } else if (strcmp(argv[i], "--source") == 0 && i+1 < argc) {
            sourcename = argv[i+1];
            i++;
        }
    }

    if (imagename == NULL || filename == NULL || sourcename == NULL) {
        fprintf(stderr, "usage: stor360fs --image <imagename> " \
            "--file <filename in image> " \
            "--source <filename on host>\n");
        exit(1);
    }
   
    open_file1(imagename,sb);
    open_file(imagename);
    
    return 0; 
}
