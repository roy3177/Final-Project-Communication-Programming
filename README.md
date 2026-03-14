# Network Traffic Analysis — Final Project
### Communication Programming Course

A Python-based network traffic analysis tool that processes Wireshark packet captures and generates statistical visualizations. Two real-world services are analyzed and compared: **YouTube** and **Wikipedia**.

---

## Overview

This project captures TCP/IP traffic from two different web services using Wireshark, exports the data as CSV, and runs automated analysis scripts that produce 7 charts per service. The goal is to study and compare how these services behave at the network layer — traffic patterns, IP distributions, TCP behavior, TLS usage, packet sizes, and flow statistics.

---

## Repository Structure

```
Final-Project-Communication-Programming/
├── src/
│   ├── YouTube.py          # Analysis script for YouTube traffic
│   └── graph_analysis.py   # Analysis script for Wikipedia traffic
├── README/
│   └── readme.pdf          # Project documentation
└── Summary(PDF)/
    └── Exp-Communication Programming Final Project.pdf  # Full project report
```

---

## What Each Script Analyzes

Both scripts produce **7 charts** from their respective traffic captures:

| # | Chart | Description |
|---|-------|-------------|
| 1 | Top IPs | Most frequent source vs. destination IP addresses |
| 2 | TCP Flags Distribution | Breakdown of TCP flag combinations (SYN, ACK, FIN, etc.) |
| 3 | TLS Server Names | Top SNI hostnames extracted from TLS handshakes |
| 4 | Packet Size Distribution | Histogram of packet lengths (log-scale Y axis) |
| 5 | Inter-Packet Time | Time deltas between successive packets |
| 6 | Top Flows by Packet Count | Most active (src, dst, protocol) flow groups |
| 7 | Top Flows by Total Bytes | Highest-volume flows by byte count |

**YouTube.py** → reads `youtube_filtered.csv`
**graph_analysis.py** → reads `wikipediaa.csv`

---

## Input Data Format

Both scripts expect a Wireshark CSV export with the following columns:

| Column | Description |
|--------|-------------|
| `Time` | Packet timestamp (seconds) |
| `Source` | Source IP address |
| `Destination` | Destination IP address |
| `Protocol` | Protocol name (TCP, TLS, etc.) |
| `Length` | Packet size in bytes |
| `Flags` | TCP flag string |
| `TLS Server Name` | SNI field (optional — TLS packets only) |

To export from Wireshark: `File → Export Packet Dissections → As CSV`

---

## Requirements

- Python 3.x
- pandas
- matplotlib

Install dependencies:

```bash
pip install pandas matplotlib
```

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/roy3177/Final-Project-Communication-Programming.git
   cd Final-Project-Communication-Programming
   ```

2. Place your Wireshark-exported CSV files in the working directory:
   - `youtube_filtered.csv` — captured YouTube traffic
   - `wikipediaa.csv` — captured Wikipedia traffic

3. Run the analysis:
   ```bash
   # YouTube traffic analysis
   python src/YouTube.py

   # Wikipedia traffic analysis
   python src/graph_analysis.py
   ```

4. Charts will display interactively via matplotlib.

---

## Key Findings

The full analysis and conclusions are documented in the project report:
`Summary(PDF)/Exp-Communication Programming Final Project.pdf`

Topics covered in the report:
- Comparison of IP diversity between YouTube and Wikipedia
- TCP flag behavior differences between streaming vs. static content
- TLS SNI patterns revealing CDN usage (YouTube) vs. direct hosting (Wikipedia)
- Packet size distributions reflecting different content delivery strategies
- Flow-level traffic dominance patterns

---

## Technologies Used

- **Wireshark** — packet capture and filtering
- **Python** — data processing and visualization
- **pandas** — CSV parsing and data manipulation
- **matplotlib** — chart generation

---


