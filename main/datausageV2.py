import psutil
import time
import datetime
import csv

## https://thepythoncode.com/article/make-a-network-usage-monitor-in-python for more info


UPDATE_DELAY = 1 # in seconds (2 minutes = 720 entries/day)
MINUTE_MODULE = 2
SECONDS_INDICTAOR = 0
bool_total = True


filename = "data_usage.csv"
headers = ["Timestamp", "Total usage", "Download","Upload", "Downlaod Speed", "Upload Speed", "Total Delta","Comments"]
def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024


# get the network I/O stats from psutil
io = psutil.net_io_counters()
# extract the total bytes sent and received
bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv

def appendToCSV(header,row):
  file =  open(filename, 'a+', newline='')
  writer = csv.writer(file)

  if file.tell() == 0:
    writer.writerow(header)
  writer.writerow(row)
  file.close()    



while True:
      # sleep for `UPDATE_DELAY` seconds
      time.sleep(UPDATE_DELAY)
      # get the stats again
      io_2 = psutil.net_io_counters()
      # new - old stats gets us the speed
      us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
      # print the total download/upload along with current speeds
      current_time = datetime.datetime.now()
      formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
      formatted_time_minutes = int(current_time.strftime("%M"))
      formatted_time_seconds = int(current_time.strftime("%S"))
      #print(formatted_time_seconds)
      str_total = get_size(io_2.bytes_sent + io_2.bytes_recv)
      total = io_2.bytes_sent + io_2.bytes_recv
      upload_data = get_size(io_2.bytes_sent)
      download_data = get_size(io_2.bytes_recv)
      upload_speed = get_size(us / UPDATE_DELAY)
      download_speed =  get_size(ds / UPDATE_DELAY)

      
      if(bool_total == True):
            initial_total = total      
            bool_total = False
      
      rows_data = [formatted_time, str_total,download_data,upload_data,download_speed,upload_speed]

      if(formatted_time_minutes % MINUTE_MODULE == 0 
         and formatted_time_seconds == SECONDS_INDICTAOR
         ):
            if( bool_total == False):
                  bool_total = True

            print(initial_total)
            print(total)
            new_total = get_size(total - initial_total)
            print(new_total)
            rows_data = rows_data + [new_total]
            print(rows_data)
            appendToCSV(headers,rows_data)

      stringPrint = f"{formatted_time}   " \
            f", Total: {str_total}   " \
            f", Download: {download_data}   " \
            f", Upload: {upload_data}   " \
            f", Download Speed: {download_speed}/s      " \
            f", Upload Speed: {upload_speed}/s   " 
      print(stringPrint)
      
       
      # update the bytes_sent and bytes_recv for next iteration
      bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv