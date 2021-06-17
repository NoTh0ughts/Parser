using MongoDB.Driver;
using Newser.DB;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Newser
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();

            var client = new MongoClient("mongodb://localhost:27017/?ssl=false");
            var db = client.GetDatabase("NewsData");

            var news = db.GetCollection<News>("News");
            var m = db.GetCollection<News>("News").AsQueryable().ToList();
            var bm = new BindingList<News>(m);
            
            if(bm.Count() > 0)
            {
                dataGridView1.DataSource = bm;
            }            
        }

        private void dataGridView1_CellMouseClick(object sender, DataGridViewCellMouseEventArgs e)
        {
            var row = e.RowIndex;

            if(dataGridView1.Rows[row].Cells[e.ColumnIndex].Value != null)
            {
                var rowData = dataGridView1.Rows[row];

                dataGridView1.CurrentRow.Selected = true;
                newsDataGroup.Enabled = true;

                idText.Text     = rowData.Cells["_Id"]?.FormattedValue.ToString();
                titleText.Text  = rowData.Cells["title"]?.FormattedValue.ToString();
                dateText.Text   = rowData.Cells["date"]?.FormattedValue.ToString();
                refText.Text    = rowData.Cells["reference"]?.FormattedValue.ToString();
                textText.Text   = rowData.Cells["text"]?.FormattedValue.ToString();
            }
            else
            {
                newsDataGroup.Enabled = false;
            }
        }

        private void refreshButton_Click(object sender, EventArgs e)
        {
            var client = new MongoClient("mongodb://localhost:27017/?ssl=false");
            var db = client.GetDatabase("NewsData");

            var news = db.GetCollection<News>("News");
            var m = db.GetCollection<News>("News").AsQueryable().ToList();
            var bm = new BindingList<News>(m);

            if (bm.Count() > 0)
            {
                dataGridView1.DataSource = bm;
            }
        }
    }
}
