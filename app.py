from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_Radit"
    )

@app.template_filter('rupiah')
def rupiah(value):
    try:
        return f"Rp {int(value):,}".replace(",", ".")
    except:
        return "Rp 0"


@app.route("/", methods=["GET", "POST"])
def transaksi_radit():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        tgl_keluar = request.form.get("tgl_keluar_radit") or None
        cursor.execute("""
            INSERT INTO transaksi_radit
            (id_pasien_radit, id_kamar_radit, total_biaya_radit, status_pembayaran_radit, tgl_radit, tgl_keluar_radit)
            VALUES (%s, %s, %s, %s, CURDATE(), %s)
        """, (
            request.form["id_pasien_radit"],
            request.form["id_kamar_radit"],
            request.form["total_biaya_radit"],
            request.form["status_pembayaran_radit"],
            tgl_keluar
        ))
        db.commit()
        db.close()
        return redirect(url_for("transaksi_radit"))

    cursor.execute("""
        SELECT t.*, p.nama_radit, k.no_kamar_radit, k.kelas_radit
        FROM transaksi_radit t
        JOIN pasien_radit p ON t.id_pasien_radit = p.id_pasien_radit
        JOIN kamar_radit k ON t.id_kamar_radit = k.id_kamar_radit
    """)
    data_radit = cursor.fetchall()
    
    cursor.execute("SELECT * FROM pasien_radit")
    pasien_list = cursor.fetchall()
    
    cursor.execute("SELECT * FROM kamar_radit")
    kamar_list = cursor.fetchall()
    
    db.close()
    return render_template("transaksi.html", data_radit=data_radit, pasien_radit=pasien_list, kamar_radit=kamar_list)

@app.route("/hapus_transaksi/<int:id>")
def hapus_transaksi(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM transaksi_radit WHERE id_transaksi_radit = %s", (id,))
    db.commit()
    db.close()
    return redirect(url_for("transaksi_radit"))

@app.route("/edit/<int:id>")
def edit_transaksi(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transaksi_radit WHERE id_transaksi_radit = %s", (id,))
    transaksi = cursor.fetchone()
    cursor.execute("SELECT * FROM pasien_radit")
    pasien = cursor.fetchall()
    cursor.execute("SELECT * FROM kamar_radit")
    kamar = cursor.fetchall()
    db.close()
    return render_template("edit_transaksi.html", transaksi=transaksi, pasien_radit=pasien, kamar_radit=kamar)

@app.route("/update/<int:id>", methods=["POST"])
def update_transaksi(id):
    db = get_db()
    cursor = db.cursor()
    tgl_keluar = request.form.get("tgl_keluar_radit") or None
    cursor.execute("""
        UPDATE transaksi_radit 
        SET id_pasien_radit=%s, id_kamar_radit=%s, total_biaya_radit=%s, 
            status_pembayaran_radit=%s, tgl_keluar_radit=%s
        WHERE id_transaksi_radit=%s
    """, (
        request.form["id_pasien_radit"],
        request.form["id_kamar_radit"],
        request.form["total_biaya_radit"],
        request.form["status_pembayaran_radit"],
        tgl_keluar,
        id
    ))
    db.commit()
    db.close()
    return redirect(url_for("transaksi_radit"))


@app.route("/pasien", methods=["GET", "POST"])
def pasien_radit():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == "POST":
        cursor.execute("INSERT INTO pasien_radit (nama_radit, alamat_radit, kontak_radit) VALUES (%s, %s, %s)", 
                       (request.form["nama_radit"], request.form["alamat_radit"], request.form["kontak_radit"]))
        db.commit()
        db.close()
        return redirect(url_for("pasien_radit"))

    cursor.execute("SELECT * FROM pasien_radit")
    data_pasien = cursor.fetchall()
    db.close()
    return render_template("pasien.html", data_pasien=data_pasien)

@app.route("/pasien/hapus/<int:id>")
def hapus_pasien(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM pasien_radit WHERE id_pasien_radit = %s", (id,))
    db.commit()
    db.close()
    return redirect(url_for("pasien_radit"))

if __name__ == "__main__":
    app.run(debug=True)
