const { google } = require("googleapis");
const { DateTime } = require("luxon");

async function getOrdersFromGoogleSheet(
  serviceAccountFile,
  spreadsheetId,
  instantOnly = false
) {
  const utcNow = DateTime.utc();
  const egyptNow = utcNow.setZone("Africa/Cairo");
  const today = egyptNow.toISODate();

  const df = await readFromGoogleSheetByDate(
    serviceAccountFile,
    spreadsheetId,
    today,
    "Today's Orders"
  );

  const couriersOrders = [];
  let currentCourier = null;
  let currentOrders = [];

  // Iterate through the rows in the DataFrame
  for (const row of df) {
    if (instantOnly && row["Order Type"].toLowerCase() !== "new order") {
      continue;
    }

    const courier = row["Courier"];
    const orderId = row["Order ID"];

    // Check if the courier changes
    if (courier !== currentCourier) {
      // Save the current list of orders if it exists
      if (currentCourier !== null) {
        couriersOrders.push([currentCourier, currentOrders]);
      }

      // Update the current courier and reset the order list
      currentCourier = courier;
      currentOrders = [];
    }

    // Add the order ID to the current list
    if (orderId && !currentOrders.includes(orderId)) {
      if (orderId.length === 9) {
        currentOrders.push(orderId);
      }
    }
  }

  // Add the last courier and their orders to the result
  if (currentCourier !== null) {
    couriersOrders.push([currentCourier, currentOrders]);
  }

  return couriersOrders;
}

async function readFromGoogleSheetByDate(
  serviceAccountFile,
  spreadsheetId,
  dateStr,
  sheetName
) {
  const auth = new google.auth.GoogleAuth({
    keyFile: serviceAccountFile,
    scopes: ["https://www.googleapis.com/auth/spreadsheets.readonly"],
  });

  const sheets = google.sheets({ version: "v4", auth });

  // Convert dateStr to a Luxon DateTime object
  const date = DateTime.fromISO(dateStr);

  // Fetch all data from the sheet
  const response = await sheets.spreadsheets.values.get({
    spreadsheetId: spreadsheetId,
    range: `${sheetName}!A1:Z`,
  });

  const rows = response.data.values;

  if (!rows || rows.length === 0) {
    throw new Error("No data found in the sheet.");
  }

  const header = rows[0];
  const data = rows.slice(1);

  // Filter data by date
  const filteredData = data
    .filter((row) => {
      const rowDateStr = row[0]; // Adjust index if date is in a different column
      try {
        const rowDate = DateTime.fromFormat(rowDateStr, "MMMM dd, yyyy");
        return rowDate.hasSame(date, "day");
      } catch {
        return false; // Skip rows with invalid date format
      }
    })
    .map((row) => {
      // Pad the row with null if its length is less than header length
      while (row.length < header.length) {
        row.push(null);
      }
      return row;
    });

  // Convert to an array of objects
  return filteredData.map((row) => {
    const obj = {};
    header.forEach((key, index) => {
      obj[key] = row[index];
    });
    return obj;
  });
}

module.exports = { getOrdersFromGoogleSheet, readFromGoogleSheetByDate };
