
// ==========================================
// INNOVAC - AI EMAIL CASE ASSISTANT
// Additional Demo Database Collections
// ==========================================


// 1. TECHNICIANS
db.technicians.insertMany([
  {
    _id: "TECH001",
    name: "Daniel Fischer",
    email: "daniel.fischer@innovac.example",
    specialization: ["CNC Machines", "Cooling Systems"],
    experience_years: 8,
    location: "Berlin",
    availability: "Available",
    skill_level: "Senior"
  },
  {
    _id: "TECH002",
    name: "Michael Braun",
    email: "michael.braun@innovac.example",
    specialization: ["Hydraulic Systems", "Industrial Presses"],
    experience_years: 12,
    location: "Hamburg",
    availability: "Busy",
    skill_level: "Expert"
  },
  {
    _id: "TECH003",
    name: "Laura Schneider",
    email: "laura.schneider@innovac.example",
    specialization: ["Electrical Systems", "Industrial Automation"],
    experience_years: 6,
    location: "Munich",
    availability: "Available",
    skill_level: "Senior"
  },
  {
    _id: "TECH004",
    name: "Peter Hoffmann",
    email: "peter.hoffmann@innovac.example",
    specialization: ["Packaging Machines", "Preventive Maintenance"],
    experience_years: 10,
    location: "Munich",
    availability: "Available",
    skill_level: "Expert"
  }
]);


// 2. SPARE PARTS
db.spare_parts.insertMany([
  {
    _id: "PART001",
    part_number: "SP-CNC-001",
    name: "Cooling System Sensor",
    compatible_models: ["IN-CNC-500"],
    description: "Temperature monitoring sensor",
    unit_price_eur: 85.50,
    supplier_id: "SUP001"
  },
  {
    _id: "PART002",
    part_number: "SP-HP-002",
    name: "Hydraulic Filter",
    compatible_models: ["IN-HP-200"],
    description: "Hydraulic filtration component",
    unit_price_eur: 45.00,
    supplier_id: "SUP002"
  },
  {
    _id: "PART003",
    part_number: "SP-CUT-003",
    name: "Electrical Control Module",
    compatible_models: ["IN-CUT-300"],
    description: "Machine control module",
    unit_price_eur: 320.00,
    supplier_id: "SUP001"
  },
  {
    _id: "PART004",
    part_number: "SP-PACK-004",
    name: "Packaging Conveyor Belt",
    compatible_models: ["IN-PACK-700"],
    description: "Replacement conveyor belt",
    unit_price_eur: 120.00,
    supplier_id: "SUP003"
  }
]);


// 3. INVENTORY
db.inventory.insertMany([
  {
    _id: "INV001",
    part_id: "PART001",
    warehouse: "Berlin",
    quantity_available: 12,
    reserved_quantity: 2,
    minimum_stock: 5
  },
  {
    _id: "INV002",
    part_id: "PART002",
    warehouse: "Hamburg",
    quantity_available: 2,
    reserved_quantity: 0,
    minimum_stock: 5
  },
  {
    _id: "INV003",
    part_id: "PART003",
    warehouse: "Berlin",
    quantity_available: 0,
    reserved_quantity: 0,
    minimum_stock: 2
  },
  {
    _id: "INV004",
    part_id: "PART004",
    warehouse: "Munich",
    quantity_available: 15,
    reserved_quantity: 3,
    minimum_stock: 5
  }
]);


// 4. MAINTENANCE PLANS
db.maintenance_plans.insertMany([
  {
    _id: "MP001",
    machine_id: "MACH001",
    customer_id: "CUST001",
    maintenance_type: "Preventive Maintenance",
    frequency: "Every 6 months",
    last_maintenance: ISODate("2026-08-15T10:00:00Z"),
    next_maintenance: ISODate("2027-02-15T10:00:00Z"),
    status: "Scheduled"
  },
  {
    _id: "MP002",
    machine_id: "MACH002",
    customer_id: "CUST001",
    maintenance_type: "Hydraulic Inspection",
    frequency: "Every 3 months",
    last_maintenance: ISODate("2026-10-11T10:00:00Z"),
    next_maintenance: ISODate("2027-01-11T10:00:00Z"),
    status: "Scheduled"
  },
  {
    _id: "MP003",
    machine_id: "MACH003",
    customer_id: "CUST002",
    maintenance_type: "Electrical Inspection",
    frequency: "Every 6 months",
    last_maintenance: ISODate("2026-06-15T10:00:00Z"),
    next_maintenance: ISODate("2026-12-15T10:00:00Z"),
    status: "Scheduled"
  }
]);


// 5. MACHINE READINGS
db.machine_readings.insertMany([
  {
    _id: "READ001",
    machine_id: "MACH001",
    temperature_celsius: 92,
    normal_temperature_range: "40-75",
    vibration_level: 8.5,
    recorded_at: ISODate("2026-11-03T08:15:00Z"),
    alert: "High temperature",
    error_code: "E-204"
  },
  {
    _id: "READ002",
    machine_id: "MACH002",
    hydraulic_pressure_bar: 85,
    normal_pressure_range: "100-150",
    recorded_at: ISODate("2026-10-10T09:00:00Z"),
    alert: "Low hydraulic pressure",
    error_code: "H-102"
  },
  {
    _id: "READ003",
    machine_id: "MACH003",
    voltage: 380,
    normal_voltage_range: "390-410",
    recorded_at: ISODate("2026-11-04T08:45:00Z"),
    alert: "Voltage below configured operating range",
    error_code: "E-310"
  },
  {
    _id: "READ004",
    machine_id: "MACH004",
    temperature_celsius: 55,
    normal_temperature_range: "40-75",
    recorded_at: ISODate("2026-11-05T09:00:00Z"),
    alert: "Normal",
    error_code: null
  }
]);


// 6. SERVICE APPOINTMENTS
db.service_appointments.insertMany([
  {
    _id: "APPT001",
    case_id: "CASE001",
    customer_id: "CUST001",
    machine_id: "MACH001",
    technician_id: "TECH001",
    appointment_date: ISODate("2026-11-07T09:00:00Z"),
    appointment_type: "On-site Inspection",
    status: "Pending Confirmation",
    notes: "Investigate CNC machine error E-204."
  },
  {
    _id: "APPT002",
    case_id: "CASE002",
    customer_id: "CUST001",
    machine_id: "MACH002",
    technician_id: "TECH002",
    appointment_date: ISODate("2026-10-11T10:00:00Z"),
    appointment_type: "Repair",
    status: "Completed",
    notes: "Hydraulic filter replacement."
  },
  {
    _id: "APPT003",
    case_id: "CASE003",
    customer_id: "CUST002",
    machine_id: "MACH003",
    technician_id: "TECH003",
    appointment_date: ISODate("2026-11-08T11:00:00Z"),
    appointment_type: "Electrical Inspection",
    status: "Scheduled",
    notes: "Investigate repeated machine shutdown."
  }
]);


// 7. WARRANTIES
db.warranties.insertMany([
  {
    _id: "WAR001",
    machine_id: "MACH001",
    customer_id: "CUST001",
    warranty_type: "Standard Warranty",
    start_date: ISODate("2025-02-01T00:00:00Z"),
    end_date: ISODate("2027-02-01T00:00:00Z"),
    coverage: [
      "Manufacturing defects",
      "Electrical components",
      "Mechanical components"
    ],
    exclusions: [
      "Accidental damage",
      "Unauthorized modifications"
    ],
    status: "Active"
  },
  {
    _id: "WAR002",
    machine_id: "MACH002",
    customer_id: "CUST001",
    warranty_type: "Standard Warranty",
    start_date: ISODate("2025-04-10T00:00:00Z"),
    end_date: ISODate("2027-04-10T00:00:00Z"),
    coverage: [
      "Hydraulic components",
      "Manufacturing defects"
    ],
    status: "Active"
  },
  {
    _id: "WAR003",
    machine_id: "MACH003",
    customer_id: "CUST002",
    warranty_type: "Extended Warranty",
    start_date: ISODate("2025-06-15T00:00:00Z"),
    end_date: ISODate("2028-06-15T00:00:00Z"),
    coverage: [
      "Electrical components",
      "Mechanical components",
      "Control systems"
    ],
    status: "Active"
  }
]);


// 8. SUPPLIERS
db.suppliers.insertMany([
  {
    _id: "SUP001",
    company_name: "Industrial Electronics GmbH",
    contact_email: "sales@electronics.example",
    location: "Berlin",
    supplied_categories: [
      "Sensors",
      "Electrical Components",
      "Control Modules"
    ]
  },
  {
    _id: "SUP002",
    company_name: "Hydraulic Systems Europe",
    contact_email: "sales@hydraulics.example",
    location: "Hamburg",
    supplied_categories: [
      "Hydraulic Filters",
      "Hydraulic Pumps"
    ]
  },
  {
    _id: "SUP003",
    company_name: "Packaging Parts Germany",
    contact_email: "sales@packaging.example",
    location: "Munich",
    supplied_categories: [
      "Conveyor Belts",
      "Packaging Components"
    ]
  }
]);


// 9. PARTS ORDERS
db.parts_orders.insertMany([
  {
    _id: "PO001",
    case_id: "CASE001",
    part_id: "PART001",
    supplier_id: "SUP001",
    quantity: 2,
    order_date: ISODate("2026-11-03T12:00:00Z"),
    expected_delivery: ISODate("2026-11-06T00:00:00Z"),
    status: "Ordered"
  },
  {
    _id: "PO002",
    case_id: "CASE002",
    part_id: "PART002",
    supplier_id: "SUP002",
    quantity: 1,
    order_date: ISODate("2026-10-10T12:00:00Z"),
    expected_delivery: ISODate("2026-10-11T00:00:00Z"),
    status: "Delivered"
  }
]);


// 10. CASE ACTIVITIES
db.case_activities.insertMany([
  {
    _id: "ACT001",
    case_id: "CASE001",
    activity_type: "Case Created",
    performed_by: "System",
    description: "Customer reported CNC machine failure.",
    created_at: ISODate("2026-11-03T08:30:00Z")
  },
  {
    _id: "ACT002",
    case_id: "CASE001",
    activity_type: "Priority Updated",
    performed_by: "Support Employee",
    description: "Priority changed to Critical because production stopped.",
    created_at: ISODate("2026-11-03T08:45:00Z")
  },
  {
    _id: "ACT003",
    case_id: "CASE001",
    activity_type: "Technician Assigned",
    performed_by: "Support Manager",
    description: "Daniel Fischer assigned to investigate the issue.",
    created_at: ISODate("2026-11-03T10:00:00Z")
  },
  {
    _id: "ACT004",
    case_id: "CASE003",
    activity_type: "Technical Escalation",
    performed_by: "Support Employee",
    description: "Repeated electrical shutdown escalated to electrical support.",
    created_at: ISODate("2026-11-04T10:00:00Z")
  }
]);


// ==========================================
// CREATE DATABASE INDEXES
// ==========================================

db.machines.createIndex({ customer_id: 1 });

db.cases.createIndex({
  customer_id: 1,
  status: 1
});

db.cases.createIndex({ machine_id: 1 });

db.emails.createIndex({
  customer_id: 1,
  created_at: -1
});

db.emails.createIndex({ case_id: 1 });

db.service_records.createIndex({ machine_id: 1 });

db.service_appointments.createIndex({
  technician_id: 1,
  status: 1
});

db.warranties.createIndex({ machine_id: 1 });

db.inventory.createIndex({ part_id: 1 });

db.machine_readings.createIndex({
  machine_id: 1,
  recorded_at: -1
});

db.case_activities.createIndex({
  case_id: 1,
  created_at: 1
});

db.knowledge_chunks.createIndex({
  machine_model: 1
});

print("==================================");
print("Innovac demo data insertion completed.");
print("10 additional collections created.");
print("Database indexes created.");
print("==================================");
