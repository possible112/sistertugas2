import asyncio
import random
import tkinter as tk
from tkinter import ttk
import threading
import time

# Global variable to hold metrics
metrics = {
    "Request-Response": {"count": 0, "total_time": 0},
    "Publish-Subscribe": {"count": 0, "total_time": 0},
    "Message Passing": {"count": 0, "total_time": 0},
    "RPC": {"count": 0, "total_time": 0},
}

# Function to log metrics
def log_metrics(model, time_taken):
    metrics[model]["count"] += 1
    metrics[model]["total_time"] += time_taken

# Request-Response Model (Asynchronous)
async def request_response_server(request_queue, response_queue, output_box, max_requests=3):
    """
    Server dalam model Request-Response.
    Fungsi ini mendengarkan permintaan dari client, memprosesnya, dan mengirimkan tanggapan kembali.
    Server mengambil request dari antrian, memprosesnya (simulasi delay), dan mengirimkan response.
    """
    while True:
        # Memeriksa apakah ada request dari client
        if not request_queue.empty():
            request = await request_queue.get()
            output_box.insert(tk.END, f"[Server] Received request: {request}\n", "server")
            await asyncio.sleep(random.uniform(0.5, 2))  # Simulate processing delay
            response = f"Response to {request}"
            await response_queue.put(response)
        await asyncio.sleep(0.1)  # Simulate server waiting for next request


async def request_response_client(request_queue, response_queue, output_box, max_requests=3):
    """
    Client dalam model Request-Response.
    Fungsi ini mengirim permintaan ke server dan menerima tanggapan.
    Client membuat request, mengirimkannya ke server, lalu menunggu response dari server.
    """
    request = "Client Request"
    output_box.insert(tk.END, f"[Client] Sending: {request}\n", "client")

    start_time = time.time()
    await request_queue.put(request)  # Mengirim request ke server
    response = await response_queue.get()  # Menunggu response dari server
    end_time = time.time()

    elapsed_time = end_time - start_time
    log_metrics("Request-Response", elapsed_time)

    output_box.insert(tk.END, f"[Client] Received: {response}\n", "client")
    output_box.insert(tk.END, f"Elapsed time for this request-response: {elapsed_time:.2f} seconds\n", "info")


# Publish-Subscribe Model (Asynchronous)
async def publisher(broker, topic, output_box):
    """
    Publisher dalam model Publish-Subscribe.
    Fungsi ini mempublikasikan pesan ke broker dalam topik tertentu.
    Publisher mengirim pesan ke topik yang terdaftar dalam broker.
    """
    for i in range(5):  # Publish multiple messages
        message = f"Message {i + 1} to topic: {topic}"
        output_box.insert(tk.END, f"[Publisher] Publishing: '{message}'\n", "publisher")
        start_time = time.time()  # Start timing
        broker[topic] = message
        await asyncio.sleep(random.uniform(0.5, 1))  # Simulate time between publishing
        end_time = time.time()  # End timing
        log_metrics("Publish-Subscribe", end_time - start_time)

async def subscriber(broker, topic, output_box):
    while True:
        if topic in broker:
            message = broker[topic]
            output_box.insert(tk.END, f"[Subscriber] Received: '{message}' from topic: '{topic}'\n", "subscriber")
            output_box.insert(tk.END, f"[Subscriber] Processing message: '{message}'...\n", "subscriber")
            await asyncio.sleep(random.uniform(1, 3))  # Simulate variable processing times
            output_box.insert(tk.END, f"[Subscriber] Finished processing message: '{message}'\n", "subscriber")
            del broker[topic]  # Remove the message after processing

# Message Passing Model
async def message_passing_sender(queue, message, output_box):
    """
    Sender dalam model Message Passing.
    Fungsi ini mengirim pesan secara langsung ke receiver melalui antrian.
    Sender menempatkan pesan ke dalam antrian yang kemudian akan diambil oleh receiver.
    """
    output_box.insert(tk.END, f"[Sender] Mengirim pesan: '{message}'\n", "sender")
    start_time = time.time()  # Start timing
    await queue.put(message)
    end_time = time.time()  # End timing
    log_metrics("Message Passing", end_time - start_time)

async def message_passing_receiver(queue, output_box):
    """
    Receiver dalam model Message Passing.
    Fungsi ini menerima pesan dari antrian yang dikirim oleh sender.
    Receiver mengambil pesan dari antrian dan memprosesnya.
    """
    while True:
        message = await queue.get()
        output_box.insert(tk.END, f"[Receiver] Mendapat pesan: '{message}'\n", "receiver")
        await asyncio.sleep(random.uniform(0.5, 2))  # Simulate processing delay

# Remote Procedure Call (RPC) Model
async def rpc_server(method_name, *args):
    """
    Server dalam model Remote Procedure Call (RPC).
    Fungsi ini mengeksekusi metode yang dipanggil oleh client dan mengembalikan hasilnya.
    Server menerima nama metode dan argumen dari client, lalu mengeksekusinya.
    """
    start_time = time.time()  # Start timing
    output_box.insert(tk.END, f"[Server] Executing: {method_name} with args: {args}\n", "rpc_server")
    await asyncio.sleep(random.uniform(1, 2))  # Simulate RPC execution time
    end_time = time.time()  # End timing
    log_metrics("RPC", end_time - start_time)
    return f"Result of {method_name}"

async def rpc_client(method_name, output_box, *args):
    """
    Client dalam model Remote Procedure Call (RPC).
    Fungsi ini memanggil metode di server dan menerima hasil eksekusi.
    Client meminta server untuk mengeksekusi fungsi tertentu dan menunggu hasil.
    """
    output_box.insert(tk.END, f"[Client] Calling RPC method: {method_name} with args: {args}\n", "client")
    result = await rpc_server(method_name, *args)
    output_box.insert(tk.END, f"[Client] Received result: {result}\n", "client")

# Asinkronous
def run_simulation(selected_model, output_box, message_input=None):
    asyncio.run(start_simulation(selected_model, output_box, message_input))

async def start_simulation(selected_model, output_box, message_input=None):
    if selected_model == "Request-Response":
        '''Membuat dua antrian: request_queue untuk mengirimkan request dari client ke server, dan response_queue untuk mengirimkan response dari server kembali ke client.
        Fungsi asyncio.gather() digunakan untuk menjalankan server dan client secara bersamaan.  
        Server mendengarkan permintaan dan client mengirimkan permintaan secara asynchronous.'''
        output_box.insert(tk.END, "Starting Request-Response Model...\n", "info")
        request_queue = asyncio.Queue()
        response_queue = asyncio.Queue()

        # Jalankan server dan client secara bersamaan
        await asyncio.gather(
            request_response_server(request_queue, response_queue, output_box),
            request_response_client(request_queue, response_queue, output_box)
        )

    elif selected_model == "Publish-Subscribe":
        '''Fungsi publisher dan subscriber dijalankan bersamaan dengan asyncio.gather(), di mana publisher akan mempublikasikan pesan ke topik yang ditentukan, 
        dan subscriber akan mendengarkan pesan dari topik tersebut melalui broker.'''
        output_box.insert(tk.END, "Starting Publish-Subscribe Model...\n", "info")
        broker = {}
        await asyncio.gather(
            publisher(broker, "topic1", output_box),
            subscriber(broker, "topic1", output_box)
        )

    elif selected_model == "Message Passing":
        '''Fungsi message_passing_sender mengirim pesan (dalam hal ini message_input yang dimasukkan oleh pengguna), 
        dan message_passing_receiver menerima pesan dari antrian tersebut dan menampilkannya di GUI.'''
        output_box.insert(tk.END, "Starting Message Passing Model...\n", "info")
        queue = asyncio.Queue()
        await asyncio.gather(
            message_passing_sender(queue, message_input, output_box),
            message_passing_receiver(queue, output_box)
        )

    elif selected_model == "RPC":
        '''Pada model RPC ini, client akan memanggil sebuah metode remote di server, dalam hal ini fungsi compute_sum dengan argumen 5 dan 10.
        Fungsi rpc_client akan menampilkan proses RPC, mengirim request ke server, menunggu hasil, dan menampilkannya di output_box.'''
        output_box.insert(tk.END, "Starting RPC Model...\n", "info")
        await rpc_client("compute_sum", output_box, 5, 10)

    display_metrics(output_box)

# Function to display metrics
def display_metrics(output_box):
    output_box.insert(tk.END, "\n--- Metrics Comparison ---\n", "info")
    for model, data in metrics.items():
        avg_time = data["total_time"] / data["count"] if data["count"] > 0 else 0
        output_box.insert(tk.END, f"{model}: Count = {data['count']}, Avg Time = {avg_time:.2f} seconds\n", "info")

# Function to start the simulation in a new thread
def start_simulation_thread():
    selected_model = model_choice.get()
    message_input = message_entry.get() if selected_model == "Message Passing" else None
    output_box.delete(1.0, tk.END)  # Clear output box
    simulation_thread = threading.Thread(target=run_simulation, args=(selected_model, output_box, message_input))
    simulation_thread.start()


def update_ui(event):
    if model_choice.get() == "Message Passing":
        message_label.pack(pady=5)
        message_entry.pack(pady=5)
    else:
        message_label.pack_forget()
        message_entry.pack_forget()

# Tkinter GUI setup
def run_tkinter():
    global root, model_choice, output_box, message_entry, message_label
    root = tk.Tk()
    root.title("Sistem Terdistribusi")
    root.geometry("800x600")

    root.configure(bg="#1A1A2E")  # Dark navy background

    label = tk.Label(root, text="Pilih model Komunikasi", font=("Arial", 14), bg="#1A1A2E", fg="#EAEAEA")
    label.pack(pady=10)

    model_choice = ttk.Combobox(root, values=["Request-Response", "Publish-Subscribe", "Message Passing", "RPC"])
    model_choice.pack(pady=10)
    model_choice.current(0)
    model_choice.bind("<<ComboboxSelected>>", update_ui)  # Bind the update function

    # Entry for message input (for Message Passing)
    message_label = tk.Label(root, text="Enter message for Message Passing:", font=("Arial", 12), bg="#1A1A2E", fg="#EAEAEA")
    message_entry = tk.Entry(root, width=50)

    # Button to start simulation
    start_button = tk.Button(root, text="Start Simulation", command=start_simulation_thread, bg="#FF6F61", fg="white")
    start_button.pack(pady=10)

    # Textbox for output
    output_box = tk.Text(root, height=20, width=80, bg="#2C2C54", fg="white", font=("Arial", 12))
    output_box.pack(pady=10)

    # Configure output box tag colors
    output_box.tag_configure("client", foreground="#FFB300")
    output_box.tag_configure("server", foreground="#5EB1FF")
    output_box.tag_configure("publisher", foreground="#FF6F61")
    output_box.tag_configure("subscriber", foreground="#FFDA79")
    output_box.tag_configure("sender", foreground="#FF8C00")
    output_box.tag_configure("receiver", foreground="#E91E63")
    output_box.tag_configure("rpc_server", foreground="#673AB7")
    output_box.tag_configure("info", foreground="#EAEAEA")

    root.mainloop()

if __name__ == "__main__":
    run_tkinter()
