import { onRequest } from "firebase-functions/v2/https";
import { setGlobalOptions } from "firebase-functions/v2";
import { initializeApp } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";
import * as logger from "firebase-functions/logger";
import cors from "cors";
import { CurrenciesResponse, CurrencyMetadata, ExchangeRates } from "./types.js";

setGlobalOptions({ maxInstances: 10 });

initializeApp();
const db = getFirestore();
const corsHandler = cors({ origin: true });

export const getCurrencies = onRequest(
  {
    memory: "256MiB",
    timeoutSeconds: 30,
  },
  async (request, response) => {
    return new Promise<void>((resolve) => {
      corsHandler(request, response, async () => {
        try {
          if (request.method !== "GET") {
            response.status(405).send("Method Not Allowed");
            return;
          }

          const currenciesSnapshot = await db.collection("currencies").get();
          const currencies: Record<string, CurrencyMetadata> = {};

          currenciesSnapshot.forEach((doc) => {
            currencies[doc.id] = doc.data() as CurrencyMetadata;
          });

          const responseData: CurrenciesResponse = { currencies };

          // Set cache headers (cache for 24 hours)
          response.set("Cache-Control", "public, max-age=86400, s-maxage=86400");
          response.status(200).json(responseData);
        } catch (error) {
          logger.error("Error fetching currencies:", error);
          response.status(500).send("Internal Server Error");
        } finally {
          resolve();
        }
      });
    });
  },
);

export const getExchangeRates = onRequest(
  {
    memory: "256MiB",
    timeoutSeconds: 30,
  },
  async (request, response) => {
    return new Promise<void>((resolve) => {
      corsHandler(request, response, async () => {
        try {
          if (request.method !== "GET") {
            response.status(405).send("Method Not Allowed");
            return;
          }

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
        } finally {
          resolve();
        }
      });
    });
  },
);
