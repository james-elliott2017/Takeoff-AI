import os
import fitz
#Used for Combining Submittal Pages with Cover Page and than Saving to a location
###############################################################################################################################
#extracts cover page file from the rest
class organize_pdf_files():
	def __init__(self,work_dir):
		self.work_dir = work_dir
		self.pdf_files = os.listdir(work_dir)
	def get_info(self):
		self.seperator_main()
		return (self.section,self.cover_page,self.non_cover_pages)
	#find cover page
	def seperator_main(self,printout=False):
		self.section,self.cover_page = self.__find_cover_page(self.pdf_files)
		self.non_cover_pages = self.__grab_non_cover_pdfs(self.pdf_files,self.cover_page)
		if printout == True:
			print(f"Section:{self.section}\nCover Page:{self.cover_page}\nNon-Cover:{self.non_cover_pages}")

	@staticmethod
	def __find_cover_page(pdf_files):
		"""helper function for seperator_main. finds cover page"""
		for pdf in pdf_files:
			lower = pdf.lower()
			if lower.find("cover") != -1:
				section = lower[0:8]
				cover_pdf_name = pdf
				return (section,cover_pdf_name)
	@staticmethod
	def __grab_non_cover_pdfs(pdf_files,cover_page_name):
		"""helper function for seperator_main. return non_cover_page"""
		pdf_files.remove(cover_page_name)
		return pdf_files

class append_pdfs(organize_pdf_files):
	def __init__(self,work_dir):
		super().__init__(work_dir)
		self.section, self.cover_pdf_name, self.non_cover_list = super().get_info()
	def combine_main(self,save_file_name=None,save_dir = None):
		"""Combines Pages with Cover Page First & Saves to Desired Location, and saves new pdf"""
		if save_dir == None:
			save_dir = self.work_dir
		if save_file_name == None:
			save_file_name = "".join([self.section,"_FINAL.pdf"])
		combined_pdf = self.__combine_docs()

		save_file_complete_path = os.path.join(save_dir,save_file_name)
		combined_pdf.save(save_file_complete_path,garbage=1)

	def __combine_docs(self):
		"""save_submittal helper function to join pdf's together into one pdf"""
		combined_doc = fitz.open()
		combined_doc.insert_pdf(self.__open_pdf(os.path.join(self.work_dir,self.cover_pdf_name))) #insert cover page

		#add non-cover pages
		for pdf_file in self.non_cover_list:
			combined_doc.insert_pdf(self.__open_pdf(os.path.join(self.work_dir,pdf_file)))
		
		return combined_doc
	@staticmethod
	def __open_pdf(pdf_location):
		output_doc = fitz.open(pdf_location)
		return output_doc
##################################################################################################################################
def multi_pdf(spec_dir,save_dir):
	"""using above class walks through an entire dir, and does a pdf save per folder in it"""
	tracker_max = len(os.listdir(spec_dir))
	for i,folder in enumerate(os.listdir(spec_dir)):
		try:
			print("%{:.2f} Complete".format((i/tracker_max)*100))
			work_dir = os.path.join(spec_dir,folder,"Final")

			single_pdf_class = append_pdfs(work_dir)
			single_pdf_class.combine_main(save_dir=save_dir)
		except:
			print("A Spec Section Failed, most likely because path isn't matching the rest or no files exist to combine")
def main():
	# work_dir = r"S:\Shared Folders\Steven\Quotes\5600\5609 - Santa Rosa Criminal Court House\Submittal & Closeout\Submittal\V1 - Pre-Construction Submittals\Spec Section Headers\27 05 00\Final"
	save_dir = r"S:\Shared Folders\Steven\Quotes\5600\5609 - Santa Rosa Criminal Court House\Submittal & Closeout\Submittal\V1 - Pre-Construction Submittals\Final_Submittals"
	spec_dir = r"S:\Shared Folders\Steven\Quotes\5600\5609 - Santa Rosa Criminal Court House\Submittal & Closeout\Submittal\V1 - Pre-Construction Submittals\Spec Section Headers"
	multi_pdf(spec_dir,save_dir)

	#To use somewhere else, make sure to change "Final" inside multi_pdf() to whatever subfolder your files that need combining are

if __name__ == '__main__':
	main()