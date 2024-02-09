from pathlib import Path

from rosbags.highlevel import AnyReader

# create reader instance and open for reading
with AnyReader([Path('D:\\Ales\\2A\\S8\\R&D\\Torrent\\udacity-dataset-2-1\\udacity-dataset-2-1\\udacity-dataset_tf_2016-10-09-05-49-13_0.bag')]) as reader:
    connections = [x for x in reader.connections if x.topic == '/imu_raw/Imu']
    for connection, timestamp, rawdata in reader.messages(connections=connections):
         msg = reader.deserialize(rawdata, connection.msgtype)
         print(msg)
