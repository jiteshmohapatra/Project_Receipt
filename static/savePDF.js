
// const { jsPDF } = window.jspdf;

// const justifications = [
//     'Diesel purchases were made from local filling stations to ensure generators and machinery at remote or project sites',
//     'Labour charges were paid to skilled and unskilled workers engaged on short notice for fabrication, assembly, or repair work.',
//     'Consumables and raw materials such as welding rods, fasteners, and basic hardware were procured locally to meet urgent project demands.',
//     'Travel expenses included local transport arrangements where Vendors provided hand-written receipts without GST components'
// ];

// function drawHeader(doc, pageWidth) {
//     const blueHeight = 30;
//     const blackHeight = 5;

//     doc.setFillColor(0, 102, 204);
//     doc.context2d.beginPath();
//     doc.context2d.moveTo(0, blueHeight);
//     doc.context2d.bezierCurveTo(
//         pageWidth / 4, blueHeight - 10,
//         pageWidth * 3 / 4, blueHeight + 10,
//         pageWidth, blueHeight
//     );
//     doc.context2d.lineTo(pageWidth, 0);
//     doc.context2d.lineTo(0, 0);
//     doc.context2d.closePath();
//     doc.context2d.fill();
 
//     doc.setFillColor(0, 0, 0);
//     doc.context2d.beginPath();
//     doc.context2d.moveTo(0, blueHeight);
//     doc.context2d.bezierCurveTo(
//         pageWidth / 4, blueHeight + blackHeight,
//         pageWidth * 3 / 4, blueHeight + blackHeight,
//         pageWidth, blueHeight
//     );
//     doc.context2d.lineTo(pageWidth, blueHeight + blackHeight);
//     doc.context2d.lineTo(0, blueHeight + blackHeight);
//     doc.context2d.closePath();
//     doc.context2d.fill();

//     doc.setFont('times', 'bold');
//     doc.setFontSize(16);
//     doc.setTextColor(0, 102, 204);
//     doc.text('BARIFLO CYBERNETICS PRIVATE LIMITED', pageWidth / 2, blueHeight + blackHeight + 10, { align: 'center' });
// }

// function drawFooter(doc, pageNumber, totalPages, pageWidth, pageHeight) {
//     doc.setFillColor(0, 102, 204);
//     doc.rect(0, pageHeight - 35, pageWidth, 35, 'F');

//     doc.setFont('times', 'bold');
//     doc.setFontSize(11);
//     doc.setTextColor(255, 255, 255);

//     const leftX = 10;
//     let leftY = pageHeight - 27;
//     doc.text('CIN - U74999OR2018PTC029923', leftX, leftY);
//     leftY += 6;
//     doc.text('Room - 207, TB I-2, KIIT TBI,', leftX, leftY);
//     leftY += 6;
//     doc.text('Bhubaneswar, Odisha, 751024', leftX, leftY);

//     const rightX = pageWidth - 10;
//     let rightY = pageHeight - 27;
//     doc.text('+91 7328021033, 9777171033', rightX, rightY, { align: 'right' });
//     rightY += 6;
//     doc.text('mrityunjay.sahu@bariflolabs.com', rightX, rightY, { align: 'right' });

//     doc.setFont('times', 'normal');
//     doc.setFontSize(9);
//     doc.text(`Page ${pageNumber} of ${totalPages}`, pageWidth / 2, pageHeight - 5, { align: 'center' });
// }

// function savePDF() {
//     try {
//         const transactionId = document.getElementById('transactionId').value.trim();
//         const amount = document.getElementById('amount').value.trim().replace(/[^\d.,]/g, '');
//         const date = document.getElementById('date').value.trim();
//         const time = document.getElementById('time').value.trim();
//         const vendor = document.getElementById('vendor').value.trim();
//         const location = document.getElementById('location').value.trim();
//         const justification = document.querySelector('input[name="justification"]:checked')?.value || '';
//         const fullName = document.getElementById('fullName').value.trim();
//         const designation = document.getElementById('designation').value.trim();
//         const contact = document.getElementById('contact').value.trim();
//         const employeeId = document.getElementById('employeeId').value.trim();
//         const signatureText = document.getElementById('signatureText').value.trim();
//         const stampInput = document.getElementById('stampImage');

//         if (!justification || !transactionId || !amount || !date || !time || !vendor || !location || !fullName || !designation || !contact || !employeeId || !signatureText) {
//             alert('Please fill all required fields.');
//             return;
//         }

//         let stampBase64 = null;
//         if (stampInput.files && stampInput.files[0]) {
//             const reader = new FileReader();
//             reader.onload = function (e) {
//                 stampBase64 = e.target.result;
//                 generatePDF();
//             };
//             reader.readAsDataURL(stampInput.files[0]);
//         } else {
//             generatePDF();
//         }

//         function generatePDF() {
//             const receiptImg1 = document.querySelector('.image-section img');
//             const receiptImg2 = document.querySelector('.page-break img');

//             const receiptBase64_1 = receiptImg1 ? receiptImg1.src : null;
//             const receiptBase64_2 = receiptImg2 ? receiptImg2.src : null;

//             const doc = new jsPDF('p', 'mm', 'a4');
//             const pageWidth = doc.internal.pageSize.getWidth();
//             const pageHeight = doc.internal.pageSize.getHeight();

//             let totalPages = 2;
//             if (receiptBase64_1) totalPages++;
//             if (receiptBase64_2) totalPages++;

//             for (let page = 1; page <= totalPages; page++) {
//                 if (page > 1) doc.addPage();
//                 drawHeader(doc, pageWidth);
//                 drawFooter(doc, page, totalPages, pageWidth, pageHeight);

//                 if (page === 1 || page === 2) {
//                     doc.setFont('times', 'normal');
//                     doc.setFontSize(12);
//                     doc.setTextColor(0, 0, 0);

//                     let y = 70;

//                     if (page === 1) {
//                         // 🔥 Page 1 content (unchanged)
//                         doc.text('To', 20, y);
//                         doc.text('The Accounts Manager', 20, y += 8);
//                         doc.text('Bariflo Cybernetics Pvt Ltd', 20, y += 8);
//                         doc.text('Bhubaneswar, Odisha, 751024', 20, y += 8);
//                         y += 10;
//                         doc.setFont('times', 'bold');
//                         doc.text('Subject: Justification for Non-GST Bill Submission under Fabrication/Consumable/raw material/travel/contingency.', 20, y, { maxWidth: 170 });
//                         y += 15;
//                         doc.setFont('times', 'normal');
//                         doc.text('Dear Sir/Madam,', 20, y);
//                         y += 10;

//                         const para1 = `I am writing to provide a formal justification for the submission of non-GST bills related to expenses incurred under the following categories: Fabrication/Consumables/Raw Materials/Travel/Contingency: Diesel Purchase/Labour Charges.`;
//                         doc.text(doc.splitTextToSize(para1, 170), 20, y);
//                         y += 10;

//                         doc.setFont('times', 'bold');
//                         doc.text(`Transaction ID:`, 20, y += 8);
//                         doc.setFont('times', 'normal');
//                         doc.text(`${transactionId}`, 65, y);

//                         doc.setFont('times', 'bold');
//                         doc.text(`Amount Rs.:`, 20, y += 6);
//                         doc.setFont('times', 'normal');
//                         doc.text(`${amount}`, 65, y);

//                         doc.setFont('times', 'bold');
//                         doc.text(`Date:`, 20, y += 6);
//                         doc.setFont('times', 'normal');
//                         doc.text(`${date}`, 65, y);

//                         doc.setFont('times', 'bold');
//                         doc.text(`Time:`, 20, y += 6);
//                         doc.setFont('times', 'normal');
//                         doc.text(`${time}`, 65, y);

//                         const para2 = `The transaction was undertaken by me in response to an urgent operational requirement. The items/services were procured from ${vendor}, located ${location}`;
//                         const para2Part2 = `. These vendors, being small-scale local suppliers, are currently not registered under the GST regime and are therefore unable to issue GST-compliant invoices.`;
//                         const para3Part3 = `The selection of these vendors was based on their immediate availability, proximity, and reliability, which were crucial given the time-sensitive nature of the requirement. Sourcing from GST-registered vendors would have caused undue delays and hindered critical operations.`;

//                         doc.text(doc.splitTextToSize(para2, 170), 20, y += 10);
//                         doc.text(doc.splitTextToSize(para2Part2, 170), 20, y += 10);
//                         doc.text(doc.splitTextToSize(para3Part3, 170), 20, y += 12);

//                         y += 25;
//                         doc.text('To Illustrate:', 20, y);
//                         y += 6;

//                         justifications.slice(0, 3).forEach(j => {
//                             const isSelected = j === justification;
//                             doc.setFont('times', isSelected ? 'bold' : 'normal');
//                             doc.setTextColor(isSelected ? 0 : 0, isSelected ? 128 : 0, isSelected ? 0 : 0);
//                             doc.text(`• ${j}`, 25, y, { maxWidth: 160 });
//                             y += 12;
//                         });
//                         doc.setTextColor(0, 0, 0);
//                     } else if (page === 2) {
//                         // 🔥 Page 2 content (unchanged)
//                         y = 70;
//                         const fourth = justifications[3];
//                         const isSelected = fourth === justification;
//                         doc.setFont('times', isSelected ? 'bold' : 'normal');
//                         doc.setTextColor(isSelected ? 0 : 0, isSelected ? 128 : 0, isSelected ? 0 : 0);
//                         doc.text(`• ${fourth}`, 20, y, { maxWidth: 170 });
//                         doc.setTextColor(0, 0, 0);

//                         doc.setFont('times', 'normal');
//                         y += 20;
//                         const para3 = `All related transactions are supported by valid non-GST invoices, duly signed and acknowledged by the respective vendors. Furthermore, the materials and services received have been verified in terms of quality and quantity by the concerned team members.`;
//                         doc.text(doc.splitTextToSize(para3, 170), 20, y);

//                         y += 25;
//                         const para4 = `In view of the above, I kindly request your consideration for the approval and reimbursement of these non-GST bills under the relevant expense categories.`;
//                         doc.text(doc.splitTextToSize(para4, 170), 20, y);

//                         y += 25;
//                         doc.text('Thank you for your understanding and continued support.', 20, y);

//                         y += 20;
//                         doc.text('Sincerely,', 20, y);

//                         doc.setFont('times', 'italic');
//                         doc.setFontSize(18);
//                         doc.text(signatureText, 20, y += 12);

//                         doc.setFont('times', 'bold');
//                         doc.setFontSize(12);
//                         doc.text('Your Full Name:', 20, y += 12);
//                         doc.setFont('times', 'normal');
//                         doc.text(fullName, 80, y);

//                         // doc.setFont('times', 'bold');
//                         // doc.text('Designation:', 20, y += 8);
//                         // doc.setFont('times', 'normal');
//                         // doc.text(designation, 80, y);

//                         // doc.setFont('times', 'bold');
//                         // doc.text('Contact Information:', 20, y += 8);
//                         // doc.setFont('times', 'normal');
//                         // doc.text(contact, 80, y);

//                         // doc.setFont('times', 'bold');
//                         // doc.text('Employee ID:', 20, y += 8);
//                         // doc.setFont('times', 'normal');
//                         // doc.text(employeeId, 80, y);

//                         if (stampBase64) {
//                             const imgWidth = 40;
//                             const imgHeight = 40;
//                             const stampY = pageHeight - imgHeight - 50;
//                             const stampX = pageWidth - imgWidth - 20;
//                             doc.addImage(stampBase64, 'PNG', stampX, stampY, imgWidth, imgHeight);
//                         }
//                     }
//                 } else if (page === 3 && receiptBase64_1) {
//                     doc.setFont('times', 'bold');
//                     doc.setFontSize(16);
//                     doc.text('Attached Receipt 1', pageWidth / 2, 50, { align: 'center' });

//                     const marginTop = 60; 
//                     const marginBottom = 50; 
//                     const availableHeight = pageHeight - marginTop - marginBottom;
//                     const availableWidth = pageWidth - 20;

//                     doc.addImage(receiptBase64_1, 'JPEG', 10, marginTop, availableWidth, availableHeight);
//                 } else if (page === 4 && receiptBase64_2) {
//                     doc.setFont('times', 'bold');
//                     doc.setFontSize(16);
//                     doc.text('Attached Receipt 2', pageWidth / 2, 50, { align: 'center' });

//                     const marginTop = 60;
//                     const marginBottom = 50;
//                     const availableHeight = pageHeight - marginTop - marginBottom;
//                     const availableWidth = pageWidth - 20;

//                     doc.addImage(receiptBase64_2, 'JPEG', 10, marginTop, availableWidth, availableHeight);
//                 }
//             }

//             const safeName = fullName.replace(/\s+/g, '_');
//             const fileName = `Justification_${safeName}_${Date.now()}.pdf`;
//             doc.save(fileName);
//             alert('PDF generated successfully.');
//         }
//     } catch (err) {
//         console.error('Error generating PDF:', err);
//         alert('Failed to generate PDF. Check console for details.');
//     }
// }

const { jsPDF } = window.jspdf || {};

const justifications = [
    'Diesel purchases were made from local filling stations to ensure generators and machinery at remote or project sites',
    'Labour charges were paid to skilled and unskilled workers engaged on short notice for fabrication, assembly, or repair work.',
    'Consumables and raw materials such as welding rods, fasteners, and basic hardware were procured locally to meet urgent project demands.',
    'Travel expenses included local transport arrangements where Vendors provided hand-written receipts without GST components'
];

function drawHeader(doc, pageWidth) {
    const blueHeight = 30;
    const blackHeight = 5;

    doc.setFillColor(0, 102, 204);
    doc.context2d.beginPath();
    doc.context2d.moveTo(0, blueHeight);
    doc.context2d.bezierCurveTo(
        pageWidth / 4, blueHeight - 10,
        pageWidth * 3 / 4, blueHeight + 10,
        pageWidth, blueHeight
    );
    doc.context2d.lineTo(pageWidth, 0);
    doc.context2d.lineTo(0, 0);
    doc.context2d.closePath();
    doc.context2d.fill();

    doc.setFillColor(0, 0, 0);
    doc.context2d.beginPath();
    doc.context2d.moveTo(0, blueHeight);
    doc.context2d.bezierCurveTo(
        pageWidth / 4, blueHeight + blackHeight,
        pageWidth * 3 / 4, blueHeight + blackHeight,
        pageWidth, blueHeight
    );
    doc.context2d.lineTo(pageWidth, blueHeight + blackHeight);
    doc.context2d.lineTo(0, blueHeight + blackHeight);
    doc.context2d.closePath();
    doc.context2d.fill();

    doc.setFont('times', 'bold');
    doc.setFontSize(16);
    doc.setTextColor(0, 102, 204);
    doc.text('BARIFLO CYBERNETICS PRIVATE LIMITED', pageWidth / 2, blueHeight + blackHeight + 10, { align: 'center' });
    doc.setFontSize(12);
    doc.text('PAYMENT VOUCHER', pageWidth / 2, blueHeight + blackHeight + 20, { align: 'center' });
}

function drawFooter(doc, pageNumber, totalPages, pageWidth, pageHeight) {
    doc.setFillColor(0, 102, 204);
    doc.rect(0, pageHeight - 35, pageWidth, 35, 'F');

    doc.setFont('times', 'bold');
    doc.setFontSize(11);
    doc.setTextColor(255, 255, 255);

    const leftX = 10;
    let leftY = pageHeight - 27;
    doc.text('CIN - U74999OR2018PTC029923', leftX, leftY);
    leftY += 6;
    doc.text('Room - 207, TB I-2, KIIT TBI,', leftX, leftY);
    leftY += 6;
    doc.text('Bhubaneswar, Odisha, 751024', leftX, leftY);

    const rightX = pageWidth - 10;
    let rightY = pageHeight - 27;
    doc.text('+91 7328021033, 9777171033', rightX, rightY, { align: 'right' });
    rightY += 6;
    doc.text('mrityunjay.sahu@bariflolabs.com', rightX, rightY, { align: 'right' });

    doc.setFont('times', 'normal');
    doc.setFontSize(9);
    doc.text(`Page ${pageNumber} of ${totalPages}`, pageWidth / 2, pageHeight - 5, { align: 'center' });
}

function readFileAsBase64(fileInput) {
    return new Promise((resolve) => {
        if (fileInput.files && fileInput.files[0]) {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = () => resolve(null);
            reader.readAsDataURL(fileInput.files[0]);
        } else {
            resolve(null);
        }
    });
}

async function savePDF(sessionId, callback) {
    if (!jsPDF) {
        console.error('jsPDF not loaded, local and CDN fallbacks failed');
        alert('❌ PDF generation library (jsPDF) not loaded. Please check your internet connection or refresh the page.');
        callback(null);
        return;
    }

    try {
        console.log('Starting savePDF for session:', sessionId);

        const transactionId = document.getElementById('credit')?.value.trim();
        const amount = document.getElementById('amount')?.value.trim();
        const date = document.getElementById('date')?.value.trim();
        const time = document.getElementById('time')?.value.trim();
        const vendor = document.getElementById('procured_from')?.value.trim();
        const location = document.getElementById('location')?.value.trim();
        const justification = document.getElementById('reason')?.value.trim();
        const fullName = document.getElementById('account_name')?.value.trim();
        const signatureText = document.getElementById('receiver_signature')?.value.trim();
        const stampInput = document.getElementById('upload_stamp');
        const receiptInput = document.getElementById('additional_receipt');

        if (!transactionId || !amount || !date || !time || !vendor || !location || !justification || !fullName || !signatureText) {
            console.warn('Missing required fields:', { transactionId, amount, date, time, vendor, location, justification, fullName, signatureText });
            alert('Please fill all required fields.');
            callback(null);
            return;
        }

        console.log('Form fields validated successfully');

        const stampBase64 = await readFileAsBase64(stampInput);
        const receiptBase64 = await readFileAsBase64(receiptInput);

        console.log('Files read:', { stampBase64: !!stampBase64, receiptBase64: !!receiptBase64 });

        const doc = new jsPDF('p', 'mm', 'a4');
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();

        let totalPages = 2;
        if (receiptBase64) totalPages++;

        for (let page = 1; page <= totalPages; page++) {
            if (page > 1) doc.addPage();
            drawHeader(doc, pageWidth);
            drawFooter(doc, page, totalPages, pageWidth, pageHeight);

            if (page === 1) {
                doc.setFont('times', 'normal');
                doc.setFontSize(12);
                doc.setTextColor(0, 0, 0);

                let y = 70;
                doc.text('To', 20, y);
                doc.text('The Accounts Manager', 20, y += 8);
                doc.text('Bariflo Cybernetics Pvt Ltd', 20, y += 8);
                doc.text('Bhubaneswar, Odisha, 751024', 20, y += 8);
                y += 10;
                doc.setFont('times', 'bold');
                doc.text('Subject: Justification for Non-GST Bill Submission under Fabrication/Consumable/raw material/travel/contingency.', 20, y, { maxWidth: 170 });
                y += 15;
                doc.setFont('times', 'normal');
                doc.text('Dear Sir/Madam,', 20, y);
                y += 10;

                const para1 = `I am writing to provide a formal justification for the submission of non-GST bills related to expenses incurred under the following categories: Fabrication/Consumables/Raw Materials/Travel/Contingency: Diesel Purchase/Labour Charges.`;
                doc.text(doc.splitTextToSize(para1, 170), 20, y);
                y += 10;

                doc.setFont('times', 'bold');
                doc.text(`Transaction ID:`, 20, y += 8);
                doc.setFont('times', 'normal');
                doc.text(`${transactionId}`, 65, y);

                doc.setFont('times', 'bold');
                doc.text(`Amount Rs.:`, 20, y += 6);
                doc.setFont('times', 'normal');
                doc.text(`${amount}`, 65, y);

                doc.setFont('times', 'bold');
                doc.text(`Date:`, 20, y += 6);
                doc.setFont('times', 'normal');
                doc.text(`${date}`, 65, y);

                doc.setFont('times', 'bold');
                doc.text(`Time:`, 20, y += 6);
                doc.setFont('times', 'normal');
                doc.text(`${time}`, 65, y);

                const para2 = `The transaction was undertaken by me in response to an urgent operational requirement. The items/services were procured from ${vendor}, located ${location}`;
                const para2Part2 = `. These vendors, being small-scale local suppliers, are currently not registered under the GST regime and are therefore unable to issue GST-compliant invoices.`;
                const para3Part3 = `The selection of these vendors was based on their immediate availability, proximity, and reliability, which were crucial given the time-sensitive nature of the requirement. Sourcing from GST-registered vendors would have caused undue delays and hindered critical operations.`;

                doc.text(doc.splitTextToSize(para2, 170), 20, y += 10);
                doc.text(doc.splitTextToSize(para2Part2, 170), 20, y += 10);
                doc.text(doc.splitTextToSize(para3Part3, 170), 20, y += 12);

                y += 25;
                doc.text('To Illustrate:', 20, y);
                y += 6;

                justifications.slice(0, 3).forEach(j => {
                    const isSelected = j === justification;
                    doc.setFont('times', isSelected ? 'bold' : 'normal');
                    doc.setTextColor(isSelected ? 0 : 0, isSelected ? 128 : 0, isSelected ? 0 : 0);
                    doc.text(`• ${j}`, 25, y, { maxWidth: 160 });
                    y += 12;
                });
                doc.setTextColor(0, 0, 0);
            } else if (page === 2) {
                let y = 70;
                const fourth = justifications[3];
                const isSelected = fourth === justification;
                doc.setFont('times', isSelected ? 'bold' : 'normal');
                doc.setTextColor(isSelected ? 0 : 0, isSelected ? 128 : 0, isSelected ? 0 : 0);
                doc.text(`• ${fourth}`, 20, y, { maxWidth: 170 });
                doc.setTextColor(0, 0, 0);

                doc.setFont('times', 'normal');
                y += 20;
                const para3 = `All related transactions are supported by valid non-GST invoices, duly signed and acknowledged by the respective vendors. Furthermore, the materials and services received have been verified in terms of quality and quantity by the concerned team members.`;
                doc.text(doc.splitTextToSize(para3, 170), 20, y);

                y += 25;
                const para4 = `In view of the above, I kindly request your consideration for the approval and reimbursement of these non-GST bills under the relevant expense categories.`;
                doc.text(doc.splitTextToSize(para4, 170), 20, y);

                y += 25;
                doc.text('Thank you for your understanding and continued support.', 20, y);

                y += 20;
                doc.text('Sincerely,', 20, y);

                doc.setFont('times', 'italic');
                doc.setFontSize(18);
                doc.text(signatureText, 20, y += 12);

                doc.setFont('times', 'bold');
                doc.setFontSize(12);
                doc.text('Your Full Name:', 20, y += 12);
                doc.setFont('times', 'normal');
                doc.text(fullName, 80, y);

                if (stampBase64) {
                    const imgWidth = 40;
                    const imgHeight = 40;
                    const stampY = pageHeight - imgHeight - 50;
                    const stampX = pageWidth - imgWidth - 20;
                    doc.addImage(stampBase64, 'PNG', stampX, stampY, imgWidth, imgHeight);
                }
            } else if (page === 3 && receiptBase64) {
                doc.setFont('times', 'bold');
                doc.setFontSize(16);
                doc.text('Attached Receipt', pageWidth / 2, 50, { align: 'center' });

                const marginTop = 60;
                const marginBottom = 50;
                const availableHeight = pageHeight - marginTop - marginBottom;
                const availableWidth = pageWidth - 20;
                doc.addImage(receiptBase64, 'JPEG', 10, marginTop, availableWidth, availableHeight);
            }
        }

        const safeName = fullName.replace(/\s+/g, '_');
        const fileName = `Justification_${safeName}_${Date.now()}.pdf`;
        console.log('Saving PDF as:', fileName);
        doc.save(fileName);

        const pdfBase64 = doc.output('datauristring').split(',')[1];
        console.log('PDF base64 generated, length:', pdfBase64.length);
        callback({ pdfBase64, fileName });
    } catch (err) {
        console.error('Error generating PDF:', err);
        alert(`❌ Failed to generate PDF: ${err.message}`);
        callback(null);
    }
}