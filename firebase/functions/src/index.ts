import {onRequest} from "firebase-functions/v2/https";
import {setGlobalOptions} from "firebase-functions/v2";
import {initializeApp} from "firebase-admin/app";
import {getFirestore} from "firebase-admin/firestore";
import * as logger from "firebase-functions/logger";
import cors from "cors";
import {CurrenciesResponse, ExchangeRates} from "./types";

// Set global options
setGlobalOptions({maxInstances: 10});

// Initialize Firebase Admin
initializeApp();
const db = getFirestore();
const corsHandler = cors({origin: true});

// Helper function to handle CORS
const withCors = (handler: (req: any, res: any) => Promise<void>) => {
  return (req: any, res: any) => {
    return new Promise<void>((resolve) => {
      corsHandler(req, res, () => {
        resolve(handler(req, res));
      });
    });
  };
};

/**
 * HTTP function to get currency metadata
 */
export const getCurrencies = onRequest({
  memory: "256MiB",
  timeoutSeconds: 30,
}, withCors(async (request, response) => {
  try {
    // Only allow GET requests
    if (request.method !== "GET") {
      response.status(405).send("Method Not Allowed");
      return;
    }

    // Get all currencies from Firestore
    const currenciesSnapshot = await db.collection("currencies").get();
    const currencies: Record<string, any> = {};

    currenciesSnapshot.forEach((doc) => {
      currencies[doc.id] = doc.data();
    });

    const responseData: CurrenciesResponse = {currencies};

    // Set cache headers (cache for 24 hours)
    response.set("Cache-Control", "public, max-age=86400, s-maxage=86400");
    response.status(200).json(responseData);
  } catch (error) {
    logger.error("Error fetching currencies:", error);
    response.status(500).send("Internal Server Error");
  }
}));

/**
 * HTTP function to get exchange rates
 */
export const getExchangeRates = onRequest({
  memory: "256MiB",
  timeoutSeconds: 30,
}, withCors(async (request, response) => {
  try {
    // Only allow GET requests
    if (request.method !== "GET") {
      response.status(405).send("Method Not Allowed");
      return;
    }

    // Get exchange rates from Firestore
    const ratesDoc = await db.collection("exchangeRates").doc("latest").get();

    if (!ratesDoc.exists) {
      response.status(404).send("Exchange rates not found");
      return;
    }

    const ratesData = ratesDoc.data() as ExchangeRates;

    // Set cache headers (cache for 1 hour)
    response.set("Cache-Control", "public, max-age=3600, s-maxage=3600");
    response.status(200).json(ratesData);
  } catch (error) {
    logger.error("Error fetching exchange rates:", error);
    response.status(500).send("Internal Server Error");
  }
}));
