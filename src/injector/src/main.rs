use clap::Parser;
use dll_syringe::{process::OwnedProcess, Syringe};

/// DLL injector with support for SirHurt API
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Process
    #[arg(short, long)]
    pid: u32,

    /// Dll path (can be relative or absolute)
    #[arg(short, long)]
    dll: String,
}

#[cfg(windows)]
fn main() {
    let args = Args::parse();
    println!("Trying to get process from PID: {}", args.pid);
    let roblox = OwnedProcess::from_pid(args.pid).expect("Failed to get process from PID");
    let syringe = Syringe::for_process(roblox);
    // Inject
    syringe
        .inject(args.dll)
        .expect("Failed to inject DLL to process");
    println!("Injected.");
}

#[cfg(not(windows))]
fn main() {
    println!("This injector only supports Windows.")
}
