import fs from "fs/promises";
import { instagramGetUrl } from "instagram-url-direct";

const DATA_FILE = "reelsData.json";
const HISTORY_FILE = "history.json";
const MAX_BATCH_SIZE = 1000;
const MAX_TOTAL_ATTEMPTS = 1000;

let results = {};
let isSaving = false;

async function saveResults() {
  if (isSaving) return; // Prevent concurrent saves
  isSaving = true;
  try {
    // Remove entries with errors before saving
    for (const [url, data] of Object.entries(results)) {
      if (data && data.error) {
        delete results[url];
      }
    }
    await fs.writeFile(DATA_FILE, JSON.stringify(results, null, 2));
    console.log(`\nData saved to ${DATA_FILE}`);
  } catch (writeErr) {
    console.error(`\nFailed to write data to ${DATA_FILE}:`, writeErr.message);
  }
  isSaving = false;
}

async function fetchReels(inputFile) {
  try {
    // Read the file containing reels URLs
    let fileContent;
    try {
      fileContent = await fs.readFile(inputFile, "utf-8");
    } catch (readErr) {
      console.error(`Failed to read ${inputFile}:`, readErr.message);
      return; // Cannot proceed without URLs
    }

    let urls = Array.from(
      new Set(
        fileContent
          .split("\n")
          .map((line) => line.trim())
          .filter(Boolean)
      )
    );

    if (urls.length === 0) {
      console.log(`No URLs found in ${inputFile}.`);
      return;
    }

    // Reverse URLs to start from last line (descending order)
    urls.reverse();

    // Load existing data from reelsData.json
    let existingData = {};
    try {
      const existingContent = await fs.readFile(DATA_FILE, "utf-8");
      existingData = JSON.parse(existingContent);
    } catch (err) {
      if (err.code === "ENOENT") {
        existingData = {};
      } else {
        console.warn(
          `Warning: Could not parse ${DATA_FILE}, starting with empty data. Error: ${err.message}`
        );
        existingData = {};
      }
    }

    // Load history data from history.json
    let historyData = {};
    try {
      const historyContent = await fs.readFile(HISTORY_FILE, "utf-8");
      historyData = JSON.parse(historyContent);
    } catch (err) {
      if (err.code === "ENOENT") {
        historyData = {};
      } else {
        console.warn(
          `Warning: Could not parse ${HISTORY_FILE}, starting with empty history. Error: ${err.message}`
        );
        historyData = {};
      }
    }

    // Combine URLs from existingData and historyData to skip
    const skipUrls = new Set([
      ...Object.keys(existingData),
      ...Object.keys(historyData),
    ]);

    // Filter out URLs that are already in existingData or historyData
    let remainingUrls = urls.filter((url) => !skipUrls.has(url));

    if (remainingUrls.length === 0) {
      console.log("No new URLs to process after filtering existing and history URLs.");
      return;
    }

    results = { ...existingData };
    let fetchedCount = 0;
    let attempts = 0;

    // Setup signal handler to save on Ctrl+C
    const handleExit = async () => {
      console.log("\nProcess interrupted. Saving fetched data...");
      await saveResults();
      process.exit();
    };

    process.on("SIGINT", handleExit);
    process.on("SIGTERM", handleExit);

    // We'll try up to MAX_TOTAL_ATTEMPTS URLs, but stop early if we fetch MAX_BATCH_SIZE successfully
    while (
      fetchedCount < MAX_BATCH_SIZE &&
      attempts < MAX_TOTAL_ATTEMPTS &&
      remainingUrls.length > 0
    ) {
      // Take next URL
      const url = remainingUrls.shift();
      attempts++;

      try {
        const data = await instagramGetUrl(url);
        results[url] = data;
        fetchedCount++;
        console.log(`Fetched data for ${url} (${fetchedCount}/${MAX_BATCH_SIZE})`);
      } catch (err) {
        console.error(`Failed to fetch data for ${url}:`, err.message);
        results[url] = { error: err.message };
      }
    }

    if (fetchedCount === 0) {
      console.log("No URLs were successfully fetched.");
    } else if (fetchedCount < MAX_BATCH_SIZE) {
      console.log(
        `Fetched only ${fetchedCount} URLs out of requested ${MAX_BATCH_SIZE} after ${attempts} attempts.`
      );
    } else {
      console.log(`Successfully fetched ${fetchedCount} URLs.`);
    }

    // Remove signal handlers after normal completion
    process.off("SIGINT", handleExit);
    process.off("SIGTERM", handleExit);

    // Save results at the end
    await saveResults();
  } catch (err) {
    console.error("Unexpected error:", err);
    // Attempt to save results on unexpected error
    await saveResults();
  }
}

// Get input filename from CLI arguments, default to "reels.txt"
const inputFile = process.argv[2] || "reels.txt";

fetchReels(inputFile);
