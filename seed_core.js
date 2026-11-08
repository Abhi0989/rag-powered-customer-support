
// ==========================================
// INNOVAC - CORE DEMO DATA
// ==========================================


// 1. CUSTOMERS
db.customers.insertMany([
  {
    _id: "CUST001",
    company_name: "Müller Industrial GmbH",
    contact_person: "Thomas Müller",
    email: "thomas.mueller@example.com",
    phone: "+49 30 12345678",
    location: "Berlin",
    customer_type: "Industrial Manufacturing"
  },
  {
    _id: "CUST002",
    company_name: "Schneider Manufacturing AG",
    contact_person: "Anna Schneider",
    email: "anna.schneider@example.com",
    phone: "+49 40 98765432",
    location: "Hamburg",
    customer_type: "Automotive Manufacturing"
  },
  {
    _id: "CUST003",
    company_name: "Weber Packaging Solutions",
    contact_person: "Markus Weber",
    email: "markus.weber@example.com",
    phone: "+49 89 55555555",
    location: "Munich",
    customer_type: "Packaging Industry"
  }
]);


// 2. MACHINES
db.machines.insertMany([
  {
    _id: "MACH001",
    customer_id: "CUST001",
    machine_name: "CNC Milling Machine",
    model: "IN-CNC-500",
    serial_number: "INV-CNC-2025-001",
    installation_date: ISODate("2025-02-01"),
    warranty_until: ISODate("2027-02-01"),
    status: "Operational"
  },
  {
    _id: "MACH002",
    customer_id: "CUST001",
    machine_name: "Hydraulic Press",
    model: "IN-HP-200",
    serial_number: "INV-HP-2025-002",
    installation_date: ISODate("2025-04-10"),
    warranty_until: ISODate("2027-04-10"),
    status: "Operational"
  },
  {
    _id: "MACH003",
    customer_id: "CUST002",
    machine_name: "Industrial Cutting Machine",
    model: "IN-CUT-300",
    serial_number: "INV-CUT-2025-003",
    installation_date: ISODate("2025-06-15"),
    warranty_until: ISODate("2028-06-15"),
    status: "Operational"
  },
  {
    _id: "MACH004",
    customer_id: "CUST003",
    machine_name: "Automatic Packaging Machine",
    model: "IN-PACK-700",
    serial_number: "INV-PACK-2025-004",
    installation_date: ISODate("2025-08-01"),
    warranty_until: ISODate("2027-08-01"),
    status: "Operational"
  }
]);


// 3. TECHNICAL CASES
db.cases.insertMany([
  {
    _id: "CASE001",
    customer_id: "CUST001",
    machine_id: "MACH001",
    case_number: "TECH-2026-001",
    category: "Machine Failure",
    error_code: "E-204",
    subject: "CNC machine stopped during production",
    description: "Machine stopped unexpectedly. Display shows E-204.",
    priority: "Critical",
    status: "Open",
    assigned_department: "Technical Support",
    resolution: null
  },
  {
    _id: "CASE002",
    customer_id: "CUST001",
    machine_id: "MACH002",
    case_number: "TECH-2026-002",
    category: "Hydraulic Problem",
    error_code: "H-102",
    subject: "Hydraulic pressure too low",
    description: "Press is not reaching the required pressure.",
    priority: "High",
    status: "Closed",
    assigned_department: "Mechanical Support",
    resolution: "Hydraulic filter replaced and pressure tested."
  },
  {
    _id: "CASE003",
    customer_id: "CUST002",
    machine_id: "MACH003",
    case_number: "TECH-2026-003",
    category: "Electrical Problem",
    error_code: "E-310",
    subject: "Machine frequently shuts down",
    description: "Machine stops after approximately 30 minutes.",
    priority: "High",
    status: "In Progress",
    assigned_department: "Electrical Support",
    resolution: null
  },
  {
    _id: "CASE004",
    customer_id: "CUST003",
    machine_id: "MACH004",
    case_number: "TECH-2026-004",
    category: "Maintenance",
    subject: "Scheduled maintenance request",
    description: "Customer requests a maintenance appointment.",
    priority: "Normal",
    status: "Open",
    assigned_department: "Service Team",
    resolution: null
  }
]);


// 4. EMAIL HISTORY
db.emails.insertMany([
  {
    _id: "EMAIL001",
    customer_id: "CUST001",
    machine_id: "MACH001",
    case_id: "CASE001",
    direction: "inbound",
    sender: "thomas.mueller@example.com",
    subject: "Urgent: CNC machine stopped",
    body: "Our CNC machine stopped during production. The display shows E-204. We restarted it but the problem remains.",
    created_at: ISODate("2026-11-03T08:30:00Z")
  },
  {
    _id: "EMAIL002",
    customer_id: "CUST001",
    machine_id: "MACH001",
    case_id: "CASE001",
    direction: "outbound",
    sender: "support@innovac.example",
    subject: "Re: CNC machine stopped",
    body: "Our technical team is reviewing the issue. Please share a photograph of the error display.",
    created_at: ISODate("2026-11-03T09:15:00Z")
  },
  {
    _id: "EMAIL003",
    customer_id: "CUST001",
    machine_id: "MACH001",
    case_id: "CASE001",
    direction: "inbound",
    sender: "thomas.mueller@example.com",
    subject: "Re: CNC machine stopped",
    body: "I have attached the error display photograph. The machine is still not operational.",
    created_at: ISODate("2026-11-04T07:45:00Z")
  },
  {
    _id: "EMAIL004",
    customer_id: "CUST002",
    machine_id: "MACH003",
    case_id: "CASE003",
    direction: "inbound",
    sender: "anna.schneider@example.com",
    subject: "Machine shutting down",
    body: "Our cutting machine shuts down after around 30 minutes. Please investigate.",
    created_at: ISODate("2026-11-04T09:00:00Z")
  }
]);


// 5. SERVICE HISTORY
db.service_records.insertMany([
  {
    _id: "SR001",
    customer_id: "CUST001",
    machine_id: "MACH001",
    case_id: "CASE001",
    service_date: ISODate("2026-08-15"),
    technician: "Daniel Fischer",
    work_performed: "Routine machine inspection.",
    observations: "Cooling system checked. No abnormalities found.",
    parts_replaced: [],
    result: "Machine operational"
  },
  {
    _id: "SR002",
    customer_id: "CUST001",
    machine_id: "MACH002",
    case_id: "CASE002",
    service_date: ISODate("2026-10-11"),
    technician: "Michael Braun",
    work_performed: "Hydraulic system inspection.",
    observations: "Hydraulic filter was blocked.",
    parts_replaced: ["Hydraulic filter"],
    result: "Pressure restored successfully"
  }
]);


// 6. TECHNICAL KNOWLEDGE
db.knowledge_chunks.insertMany([
  {
    _id: "KB001",
    title: "CNC Machine Error E-204",
    machine_model: "IN-CNC-500",
    source_type: "Technical Manual",
    text: "Fictional demonstration error E-204: possible cooling-system or temperature-monitoring fault. Stop operation and follow the approved inspection procedure. Only qualified personnel should inspect electrical components."
  },
  {
    _id: "KB002",
    title: "Hydraulic Pressure Troubleshooting",
    machine_model: "IN-HP-200",
    source_type: "Technical Manual",
    text: "Low hydraulic pressure may be caused by a blocked filter, leakage or pump problems. Qualified technicians should inspect the system according to the service manual."
  },
  {
    _id: "KB003",
    title: "Electrical Machine Shutdown",
    machine_model: "IN-CUT-300",
    source_type: "Technical Manual",
    text: "Repeated electrical shutdowns require inspection by a qualified technician. Record the error code, operating duration and machine conditions."
  },
  {
    _id: "KB004",
    title: "Technical Support Escalation",
    source_type: "Company Policy",
    text: "Critical machine failures affecting production should be escalated to technical support. Do not promise a technician visit or repair completion time until availability is confirmed."
  }
]);

print("Core Innovac demo data inserted successfully.");
