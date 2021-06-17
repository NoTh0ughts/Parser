using MongoDB.Driver;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Windows.Forms;

namespace Newser.DB
{
    class NewsService
    {
        private readonly IMongoCollection<News> _news;
        public readonly BindingList<News> News;
        public NewsService(string connectionString)
        {
            var client = new MongoClient(connectionString);
            var db = client.GetDatabase("NewsData");

            _news = db.GetCollection<News>("News");
            var m = db.GetCollection<News>("News").AsQueryable().ToList();
        }

        public ICollection<News> Get() => _news.AsQueryable().ToList();

    }
}
