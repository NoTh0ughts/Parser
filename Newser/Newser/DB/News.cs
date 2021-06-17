using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace Newser.DB
{
    class News
    {
        [BsonElement("_id")]
        public ObjectId _Id { get; set; }
        
        [BsonElement("title")]
        public string Title { get; set; }

        [BsonElement("ref")]
        public string Reference { get; set; }

        [BsonElement("date")]
        public string Date { get; set; }

        [BsonElement("text")]
        public string text { get; set; }
    }
}
