/**
 * Get all databases
 */

const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl("https://us-south.functions.appdomain.cloud/api/v1/web/668214a5-5a2a-4165-8aef-70de2097ee05/default/Get_Dealerships");

  let dbList = getDbs(cloudant);
  return { dbs: dbList };
}

function getDbs(cloudant) {
  cloudant
    .getAllDbs()
    .then((body) => {
      body.forEach((db) => {
        dbList.push(db);
      });
    })
    .catch((err) => {
      console.log(err);
    });
}