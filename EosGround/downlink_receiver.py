import io
from pathlib import Path
from typing import BinaryIO

from EosLib.format.formats.downlink_header_format import DownlinkCommandFormat, DownlinkCommand
from EosLib.format.formats.downlink_chunk_format import DownlinkChunkFormat
from EosLib.packet import Packet


class DownlinkReceiver:
    def __init__(self, downlink_header: DownlinkCommandFormat,
                 destination_dir: str = None):
        if destination_dir is None:
            # If no destination directory is provided, set it to the current directory
            self.destination_dir = Path(".")
        else:
            self.destination_dir = Path(destination_dir)

        self.file_id = downlink_header.file_id
        self.num_chunks = downlink_header.num_chunks

        self.last_chunk_received = -1

        self.file_name = f"{downlink_header.file_id}.png"

        # Concatenate file to name to create destination path and open that file for writing
        self.destination_path = self.destination_dir / self.file_name
        self.destination_file: BinaryIO = io.open(self.destination_path, "wb")

        # Track received chunks using a set
        self.received_chunks = set()

    #
    def write_chunk(self, incoming_chunk: DownlinkChunkFormat):
        # Find place in file to place chunk
        self.destination_file.seek(incoming_chunk.chunk_num*incoming_chunk.get_chunk_size())
        # Write chunk to that part
        self.destination_file.write(incoming_chunk.chunk_body)
        # Mark the chunk as received
        self.received_chunks.add(incoming_chunk.chunk_num)

    def cleanup(self):
        pass

    def get_ack(self) -> DownlinkCommandFormat:
        # Find all chunks that were not received yet
        missing_chunks = [chunk_num for chunk_num in range(self.num_chunks) if chunk_num not in self.received_chunks]
        return DownlinkCommandFormat(self.file_id, self.num_chunks, DownlinkCommand.START_ACKNOWLEDGEMENT,
                                     missing_chunks)